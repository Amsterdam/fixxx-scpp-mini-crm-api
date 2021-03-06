from geoalchemy2 import Geometry
from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from api.database import Base


# Contacts related to enhanced notes
enhanced_note_contact_table = Table('enhanced_note_contact', Base.metadata,
                                    Column('contact_id', Integer,
                                           ForeignKey('contacts.id')),
                                    Column('enhanced_note_id', Integer,
                                           ForeignKey('enhanced_notes.id'))
                                    )


# Tags related to enhanced notes
enhanced_note_tag_table = Table('enhanced_note_tag', Base.metadata,
                                Column('tag_id', Integer,
                                       ForeignKey('tags.id')),
                                Column('enhanced_note_id', Integer,
                                       ForeignKey('enhanced_notes.id'))
                                )


# Schools related to enhanced notes
enhanced_note_school_table = Table('enhanced_note_school', Base.metadata,
                                   Column('school_id', Integer,
                                          ForeignKey('schools.id')),
                                   Column('enhanced_note_id', Integer,
                                          ForeignKey('enhanced_notes.id'))
                                )


class DbContact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, index=True, primary_key=True)
    naam = Column(String, unique=True, index=True)
    email = Column(String)
    phone = Column(String)
    reference = Column(String)
    school_id = Column(Integer, ForeignKey('schools.id'))
    school = relationship("DbSchool", back_populates="contacts")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = relationship("DbNote")
    enhanced_notes = relationship(
        "DbEnhancedNote",
        secondary=enhanced_note_contact_table,
        back_populates="contacts")


class DbNote(Base):
    __tablename__ = "notes"
    id = Column(Integer, index=True, primary_key=True)
    note = Column(String)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship("DbContact", back_populates="notes")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DbSchool(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, primary_key=True)
    lrkp_id = Column(String)
    school_type = Column(String, primary_key=True)  # bso, opvang, po, vo
    brin = Column(String)
    vestigingsnummer = Column(String)
    naam = Column(String, primary_key=True, index=True)
    grondslag = Column(String)
    schoolwijzer_url = Column(String)
    onderwijsconcept = Column(String)
    heeft_voorschool = Column(Boolean, nullable=True, default=None)
    leerlingen = Column(Integer)
    address = Column(String)  # adres/adres
    postcode = Column(String)  # adres/postcode
    suburb = Column(String)  # adres/stadsdeel
    website = Column(String)  # adres/website
    email = Column(String)  # adres/email
    phone = Column(String)  # adres/telefoon
    city = Column(String)  # adres/plaats
    # coordinaten/lat & coordinaten/lon
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    contacts = relationship("DbContact")
    enhanced_notes = relationship(
        "DbEnhancedNote",
        secondary=enhanced_note_school_table,
        back_populates="schools")


class DbTag(Base):
    __tablename__ = "tags"
    id = Column(Integer, index=True, primary_key=True)
    tag = Column(String, unique=True)
    type = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    enhanced_notes = relationship(
        "DbEnhancedNote",
        secondary=enhanced_note_tag_table,
        back_populates="tags")


class DbEnhancedNote(Base):
    __tablename__ = "enhanced_notes"
    id = Column(Integer, index=True, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship("DbContact", back_populates="enhanced_notes")
    note = Column(String)
    start = Column(DateTime(timezone=True), server_default=func.now())
    end = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tags = relationship(
        "DbTag",
        secondary=enhanced_note_tag_table,
        back_populates="enhanced_notes")
    schools = relationship(
        "DbSchool",
        secondary=enhanced_note_school_table,
        back_populates="enhanced_notes")
    contacts = relationship(
        "DbContact",
        secondary=enhanced_note_contact_table,
        back_populates="enhanced_notes")