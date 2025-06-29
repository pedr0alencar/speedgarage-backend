# reviews/pagination.py
from rest_framework.pagination import LimitOffsetPagination

class DefaultLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50      # 50 objetos por página
    max_limit = 50         # protege contra consultas gigantes
