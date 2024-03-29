{% extends '_layout.html'%}
{% block content%}
<h1>Sign Up</h1>

<form method="post" action="{{url_for('users.create')}}"> 
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
<div class="form-group">
    <label for="">Username</label>
    <input type="text" class="form-control" name="user_name" placeholder="Enter username">
  </div>

  <div class="form-group">
    <label for="">Email address</label>
    <input type="email" class="form-control" name="email"  placeholder="Enter email">
    <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
  </div>

  <div class="form-group">
    <label for="">Password</label>
    <input type="password" class="form-control" name="password" placeholder="Password">
    <small id="passwordHelp" class="form-text text-muted">Password must contain a combination of uppercase, lowercase, numerals and either $#@ symbols.</small>
  </div>

  <button type="submit" class="btn btn-primary">Submit</button>
</form>

{% endblock %}