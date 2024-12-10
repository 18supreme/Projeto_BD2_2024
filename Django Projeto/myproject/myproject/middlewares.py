from django.shortcuts import redirect

class VerificarLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se a URL não está na lista de login e se o usuário não está logado
        if not request.path.startswith('/login/') and not request.session.get('user_id'):
            return redirect('login')  # Redireciona para a página de login

        response = self.get_response(request)
        return response