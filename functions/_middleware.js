// One hostname: send www.gcarosso.bio to gcarosso.bio with a permanent redirect.
// Everything else falls through to the static files.
export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === 'www.gcarosso.bio') {
    url.hostname = 'gcarosso.bio';
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
