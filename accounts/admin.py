from django.contrib import admin
from accounts.models import User, Notification, Wallet, WalletTransaction, OrganizationInvitation
from django.urls import path
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import WalletDepositForm
from django.db import transaction
from django.contrib import messages

admin.site.register(User)
admin.site.register(Notification)
admin.site.register(OrganizationInvitation)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    readonly_fields = ('balance',)
    change_form_template = 'admin/accounts/wallet/change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [path('<int:wallet_id>/deposit/', self.admin_site.admin_view(self.deposit), name='wallet-deposit')]
        return custom_urls + urls

    def deposit(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, pk=wallet_id)

        if request.method == 'POST':
            form = WalletDepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                description = form.cleaned_data['description']
                with transaction.atomic():
                    wallet.balance += amount
                    wallet.save(update_fields=['balance'])
                    WalletTransaction.objects.create(wallet=wallet, transaction_type=(WalletTransaction.TransactionType.DEPOSIT), amount=amount, description=description)
                self.message_user(request, f"{amount} added to {wallet.user}'s wallet.", messages.SUCCESS)
                return redirect('admin:accounts_wallet_change', wallet.pk)
        else:
            form = WalletDepositForm()
        context = {
            **self.admin_site.each_context(request),
            'title': 'Deposit to wallet',
            'wallet': wallet,
            'form': form,
            }
        return render(request, 'admin/accounts/wallet/deposit.html', context=context)

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'wallet',
        'transaction_type',
        'amount',
        'created_at',
    )
    list_filter = ('transaction_type', 'created_at')
    readonly_fields = (
        'wallet',
        'transaction_type',
        'amount',
        'description',
        'created_at',
    )