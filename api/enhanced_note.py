from api.models.tables import DbEnhancedNote, DbSchool, DbContact
from sqlalchemy.orm import joinedload


def get_base_query(db):
    result = db.query(
        DbEnhancedNote,
    ).options(
        joinedload(DbEnhancedNote.schools)
    ).options(
        joinedload(DbEnhancedNote.tags)
    ).options(joinedload(DbEnhancedNote.contacts)).order_by(DbEnhancedNote.start.desc())

    return result


def all(db):
    result = get_base_query(db).all()
    return result


def for_contact_by_id(id, db):
    # First get contact
    contact = db.query(DbContact).filter(DbContact.id == id).first()
    search_filter = "%{}%".format(contact.naam)
    result = get_base_query(db).filter(
            DbEnhancedNote.note.ilike(search_filter) |
            (DbEnhancedNote.contact_id == contact.id) | 
            (DbEnhancedNote.contacts.any(DbContact.id == contact.id))
        ).all()
    
    return result


def for_school_by_id(id, db):
    # First get school
    school = db.query(DbSchool).filter(DbSchool.id == id).first()
    search_filter = "%{}%".format(school.naam)
    result = get_base_query(db).filter(
        DbEnhancedNote.note.ilike(search_filter) | 
        (DbEnhancedNote.schools.any(DbSchool.id == school.id))
    ).all()

    return result
