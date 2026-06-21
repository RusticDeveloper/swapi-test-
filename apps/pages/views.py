from django.shortcuts import render


def home_landing(request):
    """
    Pantalla Inicial: Muestra las reglas, el lore y los créditos.
    """
    return render(request, "pages/inicio.html")


def vista_rankings(request):
    """
    Sección de Rankings: Tabla de posiciones de los mejores jugadores.
    """
    return render(request, "pages/rankings.html")


def vista_acerca_de(request):
    """
    Sección Acerca de: Información del proyecto y créditos técnicos.
    """
    return render(request, "pages/acerca_de.html")
    return render(request, 'pages/acerca_de.html')
