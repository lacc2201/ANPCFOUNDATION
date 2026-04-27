from django.shortcuts import render, redirect, get_object_or_404
from .models import Donacion
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def home(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo_donante = request.POST.get('email')
        monto = request.POST.get('monto')
        comprobante = request.FILES.get('comprobante')

        if not nombre or not correo_donante or not monto or not comprobante:
            messages.error(request, "Todos los campos son obligatorios")
            return redirect('home')

        donacion = Donacion.objects.create(
            nombre=nombre,
            email=correo_donante,
            monto=monto,
            comprobante=comprobante
        )

        # 🌐 dominio dinámico (sirve en local y producción)
        domain = request.build_absolute_uri('/')

        # ===============================
        # 📩 EMAIL AL DONANTE
        # ===============================
        html_donante = render_to_string('donations/email.html', {
            'nombre': nombre,
            'referencia': donacion.referencia,
        })

        email_donante = EmailMultiAlternatives(
            subject="Donación recibida - ANPC Foundation",
            body="Gracias por tu donación",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[correo_donante],
        )

        email_donante.attach_alternative(html_donante, "text/html")
        email_donante.send()

        # ===============================
        # 📩 EMAIL A LA FUNDACIÓN
        # ===============================
        html_admin = render_to_string('donations/email_admin.html', {
            'nombre': nombre,
            'correo': correo_donante,
            'monto': monto,
            'referencia': donacion.referencia,
            'domain': domain,  # 🔥 IMPORTANTE para el botón
        })

        email_admin = EmailMultiAlternatives(
            subject="Nueva donación recibida",
            body="Nueva donación",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["Foundationanpc@gmail.com"],
        )

        email_admin.attach_alternative(html_admin, "text/html")
        email_admin.send()

        messages.success(request, f"Donación enviada. Ref: {donacion.referencia}")
        return redirect('home')

    return render(request, 'donations/home.html')


def aprobar_donacion(request, referencia):
    donacion = get_object_or_404(Donacion, referencia=referencia)

    # 🔒 evitar aprobar dos veces
    if donacion.estado == 'aprobado':
        return render(request, 'donations/aprobado.html', {
            'donacion': donacion,
            'mensaje': 'Esta donación ya fue aprobada.'
        })

    # ✅ aprobar donación
    donacion.estado = 'aprobado'
    donacion.save()

    # ===============================
    # 📩 EMAIL AL DONANTE (APROBADO)
    # ===============================
    html_aprobado = render_to_string('donations/email_aprobado.html', {
        'nombre': donacion.nombre,
        'referencia': donacion.referencia,
    })

    email_aprobado = EmailMultiAlternatives(
        subject="Donación aprobada - ANPC Foundation",
        body="Tu donación fue aprobada",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[donacion.email],
    )

    email_aprobado.attach_alternative(html_aprobado, "text/html")
    email_aprobado.send()

    return render(request, 'donations/aprobado.html', {
        'donacion': donacion,
        'mensaje': 'Donación aprobada correctamente.'
    })