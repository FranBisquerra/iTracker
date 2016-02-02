# -*- encoding: utf-8 -*-
from models import Ticket
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link

class TicketTable(Table):
    id         = LinkColumn(header='Id', links=[Link(text=A('id'), viewname='issue', args=(A('id'),)),])
    creator    = Column(field='creator', header='Creador')
    user 	   = Column(field='user', header='Asignado')	
    name       = Column(field='name', header='Nombre')
    dateraised = Column(field='dateraised', header='Emisión')
    datesolved = Column(field='datesolved', header='Solucionado')
    priority   = Column(field='priority', header='Prioridad')
    state      = Column(field='state', header='Estado') 
    escalated  = Column(field='escalated', header='Escalado')
    hidden     = Column(field='hidden', header='Archivada')
    class Meta:
        model = Ticket