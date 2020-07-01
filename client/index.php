<!doctype html>
<html lang="en">

<head> 
    {% load static %}

	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<link rel="stylesheet" type="text/css" href="{% static 'css/styles.css' %}">
	<link rel="stylesheet" type="text/css" href="{% static 'css/nav.css' %}">
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap"> 
</head>

<nav>
	<ul>
		<li>
			<a href="#"><img src="{% static 'img/logo.png' %}"></a>
		</li>
		<li>
			<a class="top-sign-in" href="#">Sign in</a>
		</li>
	</ul>
</nav>

<body>
	<section>
		<div class="center-wrapper">
			<div class="flex-container">
				<div class="flex-child right">
					<img src="{% static 'img/demo-1.png' %}">
				</div>
				<div class="flex-child left" id="wcsa-section">
					<div class="title-wrapper">
						<h1>Taste Quiz</h1>
					</div>
					<div class="description-wrapper">
						<p>Who knows your listening habits the best? Quiz yourself. Quiz your friends.</p>
					</div>

					<div class="head-b-wrapper">
						<a class="head-b-generate-quiz" id="button-main" href="#">Sign in with Spotify</a>
					</div>

				</div>
			</div>
		</div>
	</div>

</section>
</body>
</html>
