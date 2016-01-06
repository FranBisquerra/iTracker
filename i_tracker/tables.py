# example/app/tables.py
from models import Ticket
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link

class TicketTable(Table):
    id = LinkColumn(header='Id', links=[Link(text=A('id'), viewname='issue', args=(A('id'),)),])
    creator = Column(field='creator', header='Creator')
    name = Column(field='name', header='Name')
    dateraised = Column(field='dateraised', header='Date raised')
    datesolved = Column(field='datesolved', header='Date solved')
    priority = Column(field='priority', header='Priority')
    class Meta:
        model = Ticket