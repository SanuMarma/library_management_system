from django.urls import path
from .views import DepositMoneyView, TransactionReportView, BorrowBookView, BookListView, ReturnBookView

urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("borrow_book/<int:id>/", BorrowBookView.as_view(), name="borrow_book"),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),

    path("borrows/", BookListView.as_view(), name="borrow_list"),
    path("return/<int:borrow_id>/", ReturnBookView.as_view(), name="return_book"),
    
]