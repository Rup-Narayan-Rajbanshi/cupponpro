from rest_framework.response import Response
from rest_framework import generics
from commonapp.models.company import Company
from commonapp.models.facility import Facility
from commonapp.serializers.facility import FacilitySerializer

class CompanyFacilityListView(generics.GenericAPIView):
    # permission_classes = []
    serializer_class = FacilitySerializer

    def get(self, request, company_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            facility_obj = Facility.objects.filter(company=company_obj[0]).order_by('-id')
            if facility_obj:
                serializer = FacilitySerializer(facility_obj, many=True, context={'request':request})
                data = {
                    'success': 1,
                    'facility': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': "Facility doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

    def post(self, request, company_id):
        if company_id == int(request.data['company']):
            serializer = FacilitySerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'facility': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to add facility."
            }
            return Response(data, status=403)

class CompanyFacilityDetailView(generics.GenericAPIView):
    # permission_classes = 
    serializer_class = FacilitySerializer

    def get(self, request, company_id, facility_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            facility_obj = Facility.objects.filter(id=facility_id, company=company_obj[0])
            if facility_obj:
                serializer = FacilitySerializer(facility_obj[0], context={'request':request})
                data = {
                    'success': 1,
                    'facility': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': "Facility doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id, facility_id):
        if company_id == int(request.data['company']):
            company_obj = Company.objects.filter(id=company_id)
            if company_obj:
                facility_obj = Facility.objects.filter(id=facility_id, company=company_obj[0])
                if facility_obj:
                    serializer = FacilitySerializer(instance=facility_obj[0], data=request.data, context={'request':request})
                    if serializer.is_valid():
                        serializer.save()
                        data = {
                            'success': 1,
                            'facility': serializer.data
                        }
                        return Response(data, status=200)
                    else:
                        data = {
                            'success': 0,
                            'message': serializer.errors
                        }
                        return Response(data, status=400)
                else:
                    data = {
                        'success': 0,
                        'message': "Facility doesn't exist."
                    }
                    return Response(data, status=404)
            else:
                data = {
                    'success': 0,
                    'message': "Company doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to edit facility."
            }
            return Response(data, status=403)

    def delete(self, request, company_id, facility_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            facility_obj = Facility.objects.filter(id=facility_id, company=company_obj[0])
            if facility_obj:
                try:
                    facility_obj[0].delete()
                    data = {
                        'success': 1,
                        'facility': "Facility deleted successfully."
                    }
                    return Response(data, status=200)
                except:
                    data = {
                        'success': 0,
                        'message': "Facility cannot be deleted."
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': "Facility doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)
