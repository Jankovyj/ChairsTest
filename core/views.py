from django.views.generic.edit import FormView
from core.models import Company
from core.forms import CheckAvailabilityForm, LeaseForm

class CheckAvailabilityFormView(FormView):
    template_name = 'check_availability.html'
    form_class = CheckAvailabilityForm
    success_url = '/lease/'

    def form_valid(self, form):
        self.request.session['start_date'] = form.cleaned_data['start_date'].isoformat()
        self.request.session['end_date'] = form.cleaned_data['end_date'].isoformat()
        return super(CheckAvailabilityFormView, self).form_valid(form)


class LeaseFormView(FormView):
    template_name = 'lease.html'
    form_class = LeaseForm
    success_url = '/success'

    def get_amount(self):
        company = Company.objects.first()
        start_date = self.request.session.get('start_date')
        end_date = self.request.session.get('end_date')
        amount = company.get_amount(start_date, end_date)
        return amount

    def get_context_data(self, **kwargs):
        amount = self.get_amount()
        context = super(LeaseFormView, self).get_context_data(**kwargs)
        context['amount'] = amount
        return context
    
    def form_valid(self, form):
        if form.cleaned_data.get('amount') > self.get_amount():
            form.add_error('amount', 'The amount may not exceed the available amount')
            return super(LeaseFormView, self).form_invalid(form)
        lease = form.save(commit = False)
        lease.company = Company.objects.first()
        lease.user = self.request.user
        lease.start_date = self.request.session.pop('start_date')
        lease.end_date = self.request.session.pop('end_date')
        lease.save()
        return super(LeaseFormView, self).form_valid(form)
