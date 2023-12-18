from django.shortcuts import render, redirect

from .forms import *


# Create your views here.
def index(request):
    return None


def create_supply(request):
    SuppliesItemsFormSet = inlineformset_factory(Supplies, SuppliesItems, fields=('product', 'quantity'), extra=1)

    if request.method == 'POST':
        supplies_form = SuppliesForm(request.POST)
        if supplies_form.is_valid():
            supplies = supplies_form.save()
            supplies_items_formset = SuppliesItemsFormSet(request.POST, instance=supplies)

            if supplies_items_formset.is_valid():
                supplies_items_formset.save()
                return redirect('supply_list')
    else:
        supplies_form = SuppliesForm()
        supplies_items_formset = SuppliesItemsFormSet(instance=Supplies())

    return render(request, 'create_order.html',
                  {'supplies_form': supplies_form, 'supplies_items_formset': supplies_items_formset})


def supply_list(request):
    supplies = Supplies.objects.all()
    return render(request, 'supply_list.html', {'supplies': supplies})
