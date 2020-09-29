from rest_framework import generics
from rest_framework.response import Response
from commonapp.models.company import Company
from commonapp.models.document import Document
from commonapp.serializers.document import DocumentSerializer
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll

class CompanyDocumentListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = DocumentSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's documents.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            document_obj = Document.objects.filter(company=company_id).order_by('-id')
            serializer = DocumentSerializer(document_obj, many=True, context={'request':request})
            data = {
                'success': 1,
                'document': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's document.
        """
        if company_id == int(request.data['company']):
            serializer = DocumentSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'document': serializer.data
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
                'message': "You don't have permission to add document."
            }
            return Response(data, status=403)

class CompanyDocumentDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = DocumentSerializer

    def get(self, request, company_id, document_id):
        """
        An endpoint for getting vendor's document detail.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            document_obj = Document.objects.filter(id=document_id, company=company_id)
            if document_obj:
                serializer = DocumentSerializer(document_obj[0], context={'request':request})
                data = {
                    'success': 1,
                    'document': serializer.data
                }
                return Response(data, status=200)
            else:data = {
                'success': 0,
                'message': "Document doesn't exist."
            }
            return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id, document_id):
        """
        An endpoint for updating vendor's document detail.
        """
        if company_id == int(request.data['company']):
            company_obj = Company.objects.filter(id=company_id)
            if company_obj:
                document_obj = Document.objects.filter(id=document_id, company=company_id)
                if document_obj:
                    serializer = DocumentSerializer(instance=document_obj[0], data=request.data, context={'request':request})
                    if 'document' in request.data and not request.data['document']:
                        serializer.exclude_fields(['document'])
                    if serializer.is_valid():
                        serializer.save()
                        data = {
                            'success': 1,
                            'document': serializer.data
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
                        'message': "Document doesn't exist."
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
                'message': "You don't have permission to update document."
            }
            return Response(data, status=403)

    def delete(self, request, company_id, document_id):
        """
        An endpoint for deleting vendor's document.
        """
        document_obj = Document.objects.filter(id=document_id, company=company_id)
        if document_obj:
            try:
                document_obj[0].delete()
                data = {
                    'success': 1,
                    'document': "Document deleted successfully."
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': "Document cannot be deleted."
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Document doesn't exist."
            }
            return Response(data, status=404)
