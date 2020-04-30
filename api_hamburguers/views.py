from .models import Hamburguesa, Ingrediente
from .serializers import HamburguesaSerializer, IngredienteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['GET', 'POST'])
def hamburguer_list(request):
    if request.method == 'GET': #OK
        hamburguers = Hamburguesa.objects.all()
        serializer = HamburguesaSerializer(hamburguers, many=True) 

        for index,h in enumerate(serializer.data):
            for index_2,i in enumerate(h['ingredientes']):                
                serializer.data[index]['ingredientes'][index_2] = {'path': f"https://hamburgueseria.com/ingrediente/{i}"}
            
        return Response({'message': 'Hamburguesas', 'body': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST': #OK
        serializer = HamburguesaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Hamburguesa creada ', 'body': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Input invalido ', 'body': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def hamburguer_detail(request,pk):
    
    aux = pk.isdigit()
    if aux == False:
        return Response({'message': 'id invalido '}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        hamburguer = Hamburguesa.objects.get(pk=pk)
    
    except:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': #OK
        
        serializer = HamburguesaSerializer(hamburguer)

        for index,i in enumerate(serializer.data['ingredientes']):                
            serializer.data['ingredientes'][index] = {'path': f"https://hamburgueseria.com/ingrediente/{i}"}
        
        return Response({'message': 'Operacion exitosa ', 'body': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PATCH': #OK (REVISAR SI EL ID FUE CAMBIADO O NO)
        
        serializer = HamburguesaSerializer(hamburguer, data=request.data)
        if serializer.is_valid():
            serializer.save()

            for index,i in enumerate(serializer.data['ingredientes']):                
                serializer.data['ingredientes'][index] = {'path': f"https://hamburgueseria.com/ingrediente/{i}"}

            return Response({'message': 'Operacion exitosa ', 'body': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Parámetros invalidos ', 'body': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': #OK
        hamburguer.delete()
        return Response({'message: Hamburguesa eliminada'},status = status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def ingredient_list(request): #OK
    if request.method == 'GET': #OK
        ingredients = Ingrediente.objects.all()
        serializer = IngredienteSerializer(ingredients, many=True)
        return Response({'message': 'Operacion exitosa ', 'body': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST': #OK
        serializer = IngredienteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ingrediente creado ', 'body': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Input invalido ', 'body': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
def ingredient_detail(request,pk): #OK

    try:
        ingredient = Ingrediente.objects.get(pk=pk)
    
    except:

        return Response({'message': 'Id invalido '}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': #OK
        serializer = IngredienteSerializer(ingredient)
        return Response({'message': 'Operacion exitosa ', 'body': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE': #OK

        if Hamburguesa.objects.filter(ingredientes=ingredient).exists():
            return Response({'message: Ingrediente no se puede eliminar, se encuentra en una hamburguesa'},status = status.HTTP_409_CONFLICT)
        else:
            ingredient.delete()
            return Response({'message: Ingrediente eliminado'},status = status.HTTP_200_OK)
        

@api_view(['GET','PUT', 'DELETE'])
def hamburguer_ingredient(request,pk_h,pk_i):
    
    try:
        hamburguer = Hamburguesa.objects.get(pk=pk_h)
    
    except:
        return Response({'message': 'Hamburguesa no valida '},status=status.HTTP_400_BAD_REQUEST)

    try:
        ingredient = Ingrediente.objects.get(pk=pk_i)
    
    except:
        return Response({'message': 'Ingrediente no existe '},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': #OK
        ingredients = Ingrediente.objects.filter(pk=pk_i)
        hamburguer = Hamburguesa.objects.filter(pk=pk_h)
        serializer_i = IngredienteSerializer(ingredients, many=True)
        serializer_h = HamburguesaSerializer(hamburguer, many=True)

        for index,h in enumerate(serializer_h.data):
            for index_2,i in enumerate(h['ingredientes']):                
                serializer_h.data[index]['ingredientes'][index_2] = {'path': f"https://hamburgueseria.com/ingrediente/{i}"}
       

        return Response({'message': 'Operacion exitosa ', 'body': {'hamburguesa': serializer_h.data, 'ingrediente': serializer_i.data}}, status=status.HTTP_200_OK)

    if request.method == 'PUT': #OK
        hamburguer.ingredientes.add(ingredient)
        ingredients = Ingrediente.objects.filter(pk=pk_i)
        hamburguer = Hamburguesa.objects.filter(pk=pk_h)
        serializer_i = IngredienteSerializer(ingredients, many=True)
        serializer_h = HamburguesaSerializer(hamburguer, many=True)

        for index,h in enumerate(serializer_h.data):
            for index_2,i in enumerate(h['ingredientes']):                
                serializer_h.data[index]['ingredientes'][index_2] = {'path': f"https://hamburgueseria.com/ingrediente/{i}"}
            
        return Response({'message': 'Ingrediente agregado', 'body': {'hamburguesa': serializer_h.data, 'ingrediente': serializer_i.data}}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE': #OK

        ingredients = Ingrediente.objects.filter(pk=pk_i)
        hamburguer = Hamburguesa.objects.filter(pk=pk_h)
        serializer_i = IngredienteSerializer(ingredients, many=True)
        serializer_h = HamburguesaSerializer(hamburguer, many=True)
        hamburguer.first().ingredientes.remove(ingredient)

        for index,h in enumerate(serializer_h.data):
            for index_2,i in enumerate(h['ingredientes']):                
                serializer_h.data[index]['ingredientes'][index_2] = {'path': f"https://hamburgueseria.com/ingrediente/{i}"}

        return Response({'message': 'Ingrediente retirado', 'body': {'hamburguesa': serializer_h.data, 'ingrediente': serializer_i.data}}, status=status.HTTP_200_OK)