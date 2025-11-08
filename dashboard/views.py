from ast import Not, With
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import AccountDetail, Deposit, Transfer, Withdraw
from django.db.models import F
from django.contrib.auth.hashers import check_password

# Create your views here.


def dashboard_views(request):
    template = "dashboard.html"
    return render(request, template)


def dashboard(request):
    user = request.user
    accounts = AccountDetail.objects.filter(account_holder=user)
    history = Transfer.objects.filter(sending_user=user)
    deposit = Transfer.objects.filter(reciver_username=user)
    withdraw = Withdraw.objects.filter(sender=user)

    # Latest 3 transactions for notifications
    latest_deposit = Transfer.objects.filter(reciver_username=user).order_by("-id")[:3]
    latest_withdraw = Withdraw.objects.filter(sender=user).order_by("-id")[:3]
    latest_history = Transfer.objects.filter(sending_user=user).order_by("-id")[:3]

    # Unread chat messages
    from chat.models import ChatMessage

    unread_count = (
        ChatMessage.objects.filter(receiver=user, is_read=False)
        .exclude(sender=user)
        .count()
    )

    return render(
        request,
        "dashboard.html",
        {
            "details": accounts,
            "history": history,
            "deposit": deposit,
            "withdraw": withdraw,
            "latest_deposit": latest_deposit,
            "latest_withdraw": latest_withdraw,
            "latest_history": latest_history,
            "unread_chat_count": unread_count,
        },
    )


def send_procced(request):
    template = "send_msg.html"
    return render(request, template)


def transfer(request):

    if request.method == "POST":
        transfer_amount = request.POST["amount"]
        reciver_username = request.POST["acct_name"]
        reciver_account_number = request.POST["acct_num"]
        sender = request.user
        # sender_password = request.POST['password']
        sender_pass = request.user.password
        auth_user = User.objects.get(username=sender, password=sender_pass)

        if auth_user:
            try:
                auth_reciver = User()
                auth_reciver = User.objects.get(username=reciver_username)
                model_1 = AccountDetail.objects.get(
                    account_number=reciver_account_number
                )

                if model_1:
                    model_2 = Transfer.objects.all()
                    if auth_reciver.username == reciver_username:
                        model_2.create(
                            sending_user=sender,
                            reciver_account=reciver_account_number,
                            reciver_username=reciver_username,
                            amount=transfer_amount,
                        )
                        if model_2:
                            sender_detail = AccountDetail.objects.get(
                                account_holder=sender
                            )
                            reciver_detail = AccountDetail.objects.get(
                                account_number=reciver_account_number
                            )
                            if sender_detail.account_balance >= float(transfer_amount):

                                sender_detail.account_balance = F(
                                    "account_balance"
                                ) - float(transfer_amount)
                                reciver_detail.account_balance = F(
                                    "account_balance"
                                ) + float(transfer_amount)

                                sender_detail.save()
                                reciver_detail.save()
                                return redirect("send_proceed")
                            elif sender_detail.account_balance < float(transfer_amount):
                                return render(request, "sender_details_error.html")
                        else:  # for if model_2
                            return render(request, "model_2_error.html")
                    else:  # for if auth_reciver
                        return render(request, "auth_reciver_error.html")
                else:  # for if model_1
                    return render(request, "model_1_error.html")
            except BaseException:
                if TypeError:
                    return render(request, "auth_reciver_error.html")
                return render(request, "auth_reciver_error.html")
        else:  # for auth_user
            return render(request, "auth_user_error.html")

    return render(request, "send_form.html")


def withdraw_msg(request):
    return render(request, "withdrawal_msg.html")


def withdraw(request):
    if request.method == "POST":
        account_owner = AccountDetail.objects.get(account_holder=request.user)
        amount = request.POST["amount"]
        account_number = request.POST["acct_num"]
        bank_name = request.POST["bank_name"]

        if account_owner.account_verified:
            if account_owner.account_ready:
                model = Withdraw.objects.all()
                if account_owner.account_balance < float(amount):
                    return render(request, "sender_details_error.html")
                else:
                    model.create(
                        sender=request.user,
                        amount=amount,
                        account_number=account_number,
                        bank_name=bank_name,
                    )
                    account_owner.account_balance = F("account_balance") - amount
                    account_owner.save()
                    return render(request, "withdraw_success.html")
            else:
                return render(request, "account_not_ready.html")
        else:
            return render(request, "account_not_verified.html")
    return render(request, "withdraw.html")


def deposit(request):
    if request.method == "POST":
        depositor = request.user
        amount = request.POST["amount"]
        try:
            if depositor:
                model = Deposit.objects.all()
                model.create(account_holder=depositor, amount=amount)
                return render(request, "deposit_msg.html")
        except ValueError:
            return render(request, "value_error.html")
    return render(request, "deoposit_form.html")
