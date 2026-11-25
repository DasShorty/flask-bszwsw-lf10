from datetime import datetime

from flask import Blueprint, render_template, request, abort
from sqlalchemy import select, func

from ..models import MixingPlant, db

mixing_bp = Blueprint("mixing", __name__, url_prefix="/")

PER_PAGE = 50


def parse_dt(value: str | None, name: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        abort(400, description=f"Ungültiges Datum für '{name}'")


@mixing_bp.get("/")
def list_entries():
    von_raw = request.args.get("von", "").strip()
    bis_raw = request.args.get("bis", "").strip()
    order = request.args.get("order", "desc")
    page = max(request.args.get("page", 1, type=int), 1)

    von = parse_dt(von_raw, "von")
    bis = parse_dt(bis_raw, "bis")

    filters = []
    if von:
        filters.append(MixingPlant.timestamp >= von)
    if bis:
        filters.append(MixingPlant.timestamp <= bis)

    total = db.session.scalar(select(func.count(MixingPlant.id)).where(*filters))

    order_col = MixingPlant.timestamp.asc() if order == "asc" else MixingPlant.timestamp.desc()
    stmt = (
        select(MixingPlant)
        .where(*filters)
        .order_by(order_col)
        .limit(PER_PAGE)
        .offset((page - 1) * PER_PAGE)
    )
    entries = db.session.scalars(stmt).all()

    return render_template(
        "mixplant/list.html",
        entries=entries,
        page=page,
        pages=max((total + PER_PAGE - 1) // PER_PAGE, 1),
        total=total,
        von=von_raw,
        bis=bis_raw,
        order=order,
    )


@mixing_bp.get("/latest")
def latest_entry():
    entry = db.session.scalars(
        select(MixingPlant).order_by(MixingPlant.timestamp.desc()).limit(1)
    ).first()
    return render_template("mixplant/latest.html", entry=entry)


@mixing_bp.get("/<int:entry_id>")
def get_entry(entry_id: int):
    entry = db.session.get(MixingPlant, entry_id)
    if entry is None:
        abort(404, description="Eintrag nicht gefunden")
    return render_template("mixplant/detail.html", entry=entry)

import random
from datetime import timedelta

@mixing_bp.cli.command("seed")
def seed():
    """Erzeugt 48 h Testdaten im 5-Minuten-Takt."""
    now = datetime.now()
    fill = 80.0
    for i in range(576):
        fill -= random.uniform(0, 0.4)
        if fill < 10:
            fill = 95.0
        db.session.add(MixingPlant(
            timestamp=now - timedelta(minutes=5 * (576 - i)),
            temperature=round(random.uniform(19, 26), 2),
            humidity=round(random.uniform(35, 65), 2),
            fill_level=round(fill, 2),
        ))
    db.session.commit()
    print("576 Testeinträge angelegt.")