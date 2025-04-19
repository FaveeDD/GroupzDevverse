class ContentSecurityPolicyMiddleware:
      def __init__(self, get_response):
          self.get_response = get_response

      def __call__(self, request):
          response = self.get_response(request)
          response["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self';"
          return response

class HSTSHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        return response

class XContentTypeOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        return response