// JavaScript Document

function generarClave(longitud)
{
  var caracteres = "abcdefghijkmnpqrtuvwxyzABCDEFGHIJKLMNPQRTUVWXYZ2346789";
  var clave = "";
  for (i=0; i<longitud; i++) clave += caracteres.charAt(Math.floor(Math.random()*caracteres.length));

  document.formClave.claveNueva1.value = clave;
  document.formClave.claveNueva2.value = clave;

  return ;
}

