{% extends 'layout.html' %}
{% block title %} Tabla de Provedores {% endblock %}
{% block content %}
<div class="w3-container">
	<div clas="w3-row">
		<div class="w3-container w3-threequarter">
  			<h2>Tabla de Provedores</h2>
  		</div>
  		<div class="w3-container w3-quarter w3-padding-16">
    		<form action="/">
		    	<input type="text" placeholder="Search.." name="search">
		      	<button type="submit"><i class="fa fa-search"></i></button>
		    </form>
  		</div>
  	</div>
  <table class="w3-table-all">
    <thead>
      <tr class="w3-black">
        <th>Rut Provedor</th>
        <th>Nombre del Provedor</th>
        <th>Ciudad</th>
        <th>Comuna</th>
        <th>Correo</th>
        <th>Numero Contacto</th>
      </tr>
    </thead>
    <tr class="w3-hover-green">
      {% for array in provedores %}
      <td>{{ array['rut'] }}</td>
      <td>{{ array['nombre'] }}</td>
      <td>{{ array['ciudad'] }}</td>
      <td>{{ array['comuna'] }}</td>
      <td>{{ array['correo'] }}</td>
      <td>{{ array['telefono'] }}</td>
    </tr>
    {% endfor %}
  </table>
</div>
{% endblock %}	