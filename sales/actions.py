from sales.models.trade import TradeSession

class TradeSessionAction:
    def __init__(self, stock_point, opened_by, closed_by, open_date, close_date):
        self.stock_point = stock_point
        self.opened_by = opened_by
        self.closed_by = closed_by
        self.open_date = open_date
        self.close_date = close_date
    
    def create(self):
        if self.stock_point is None:
            raise Exception('Stock point is required')
        
        _sessions = TradeSession.objects.filter(stock_point=self.stock_point, close_date=None, opened_by=self.opened_by)
        
        if _sessions.count() > 0:
            raise Exception('Session is already opened')
        
        _session = TradeSession.objects.create(
            stock_point=self.stock_point,
            opened_by=self.opened_by,
            closed_by=self.closed_by,
            open_date=self.open_date,
            close_date=self.close_date
        )
        
        return _session
