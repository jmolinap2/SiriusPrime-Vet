from django.urls import path

from core.clinic.views.breed_pet.views import *
from core.clinic.views.canton.views import *
from core.clinic.views.category.views import *
from core.clinic.views.client.views import *
from core.clinic.views.color.views import *
from core.clinic.views.country.views import *
from core.clinic.views.employee.views import *
from core.clinic.views.mascot.views import *
from core.clinic.views.medical_parameter.views import *
from core.clinic.views.parish.views import *
from core.clinic.views.pet_history.views import *
from core.clinic.views.product.views import *
from core.clinic.views.profession.views import *
from core.clinic.views.provider.views import *
from core.clinic.views.province.views import *
from core.clinic.views.purchase.views import *
from core.clinic.views.sale.views import *
from core.clinic.views.sub_category.views import *
from core.clinic.views.type_pet.views import *
from core.clinic.views.company.views import *

urlpatterns = [
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # profession
    path('profession/', ProfessionListView.as_view(), name='profession_list'),
    path('profession/add/', ProfessionCreateView.as_view(), name='profession_create'),
    path('profession/update/<int:pk>/', ProfessionUpdateView.as_view(), name='profession_update'),
    path('profession/delete/<int:pk>/', ProfessionDeleteView.as_view(), name='profession_delete'),
    # province
    path('province/', ProvinceListView.as_view(), name='province_list'),
    path('province/add/', ProvinceCreateView.as_view(), name='province_create'),
    path('province/update/<int:pk>/', ProvinceUpdateView.as_view(), name='province_update'),
    path('province/delete/<int:pk>/', ProvinceDeleteView.as_view(), name='province_delete'),
    # canton
    path('canton/', CantonListView.as_view(), name='canton_list'),
    path('canton/add/', CantonCreateView.as_view(), name='canton_create'),
    path('canton/update/<int:pk>/', CantonUpdateView.as_view(), name='canton_update'),
    path('canton/delete/<int:pk>/', CantonDeleteView.as_view(), name='canton_delete'),
    # parish
    path('parish/', ParishListView.as_view(), name='parish_list'),
    path('parish/add/', ParishCreateView.as_view(), name='parish_create'),
    path('parish/update/<int:pk>/', ParishUpdateView.as_view(), name='parish_update'),
    path('parish/delete/<int:pk>/', ParishDeleteView.as_view(), name='parish_delete'),
    # country
    path('country/', CountryListView.as_view(), name='country_list'),
    path('country/add/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # subcategory
    path('sub/category/', SubCategoryListView.as_view(), name='sub_category_list'),
    path('sub/category/add/', SubCategoryCreateView.as_view(), name='sub_category_create'),
    path('sub/category/update/<int:pk>/', SubCategoryUpdateView.as_view(), name='sub_category_update'),
    path('sub/category/delete/<int:pk>/', SubCategoryDeleteView.as_view(), name='sub_category_delete'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # purchases
    path('purchase/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    # clients
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    # employees
    path('employee/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employee/update/profile/', EmployeeUpdateProfileView.as_view(), name='employee_update_profile'),
    # typepet
    path('type/pet/', TypePetListView.as_view(), name='type_pet_list'),
    path('type/pet/add/', TypePetCreateView.as_view(), name='type_pet_create'),
    path('type/pet/update/<int:pk>/', TypePetUpdateView.as_view(), name='type_pet_update'),
    path('type/pet/delete/<int:pk>/', TypePetDeleteView.as_view(), name='type_pet_delete'),
    # breedpet
    path('breed/pet/', BreedPetListView.as_view(), name='breed_pet_list'),
    path('breed/pet/add/', BreedPetCreateView.as_view(), name='breed_pet_create'),
    path('breed/pet/update/<int:pk>/', BreedPetUpdateView.as_view(), name='breed_pet_update'),
    path('breed/pet/delete/<int:pk>/', BreedPetDeleteView.as_view(), name='breed_pet_delete'),
    # mascot/
    path('mascot/', MascotListView.as_view(), name='mascot_list'),
    path('mascot/add/', MascotCreateView.as_view(), name='mascot_create'),
    path('mascot/update/<int:pk>/', MascotUpdateView.as_view(), name='mascot_update'),
    path('mascot/delete/<int:pk>/', MascotDeleteView.as_view(), name='mascot_delete'),
    # mascot/client
    path('mascot/client/', MascotClientListView.as_view(), name='mascot_client_list'),
    path('mascot/client/add/', MascotClientCreateView.as_view(), name='mascot_client_create'),
    path('mascot/client/update/<int:pk>/', MascotClientUpdateView.as_view(), name='mascot_client_update'),
    path('mascot/client/delete/<int:pk>/', MascotClientDeleteView.as_view(), name='mascot_client_delete'),
    # color
    path('color/', ColorListView.as_view(), name='color_list'),
    path('color/add/', ColorCreateView.as_view(), name='color_create'),
    path('color/update/<int:pk>/', ColorUpdateView.as_view(), name='color_update'),
    path('color/delete/<int:pk>/', ColorDeleteView.as_view(), name='color_delete'),
    # medical parameters
    path('medical/parameter/', MedicalParameterListView.as_view(), name='medical_parameter_list'),
    path('medical/parameter/add/', MedicalParameterCreateView.as_view(), name='medical_parameter_create'),
    path('medical/parameter/update/<int:pk>/', MedicalParameterUpdateView.as_view(), name='medical_parameter_update'),
    path('medical/parameter/delete/<int:pk>/', MedicalParameterDeleteView.as_view(), name='medical_parameter_delete'),
    # sale
    path('sale/', SaleListView.as_view(), name='sale_list'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_print_invoice'),
    path('sale/client/', SaleClientListView.as_view(), name='sale_client_list'),
    path('sale/client/add/', SaleClienCreateView.as_view(), name='sale_client_create'),
    path('sale/client/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_client_print_invoice'),
    path('sale/employee/', SaleEmployeeListView.as_view(), name='sale_employee_list'),
    path('sale/employee/add/', SaleEmployeeCreateView.as_view(), name='sale_employee_create'),
    path('sale/employee/attend/<int:pk>/', SaleEmployeeCreateView.as_view(), name='sale_employee_attend'),
    path('sale/employee/delete/<int:pk>/', SaleEmployeeDeleteView.as_view(), name='sale_employee_delete'),
    path('sale/employee/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_employee_print_invoice'),
    # pet/history
    path('pet/history/vaccines/', PetHistoryVaccinesListView.as_view(), name='pet_history_vaccines_list'),
    path('pet/history/client/vaccines/', PetHistoryVaccinesListView.as_view(), name='pet_history_client_vaccines_list'),
    path('pet/history/medical/', PetHistoryMedicalListView.as_view(), name='pet_history_medical_list'),
    path('pet/history/client/medical/', PetHistoryMedicalListView.as_view(), name='pet_history_client_medical_list'),
]
