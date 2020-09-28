def generate_vizgen_html(time_EST):
    print("Generating stats page HTML...")
    vizgen_html = f"""
        <!doctype html>
        <html lang="en">

            <head>
                <!-- Global site tag (gtag.js) - Google Analytics -->
                <script async src="https://www.googletagmanager.com/gtag/js?id=UA-177618781-1"></script>
                <script>
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){{dataLayer.push(arguments);}}
                    gtag('js', new Date());
                    gtag('config', 'UA-177618781-1');
                </script>
                
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <script src="plot.js"></script>

                <meta content="width=device-width, initial-scale=1" name="viewport" />
                <link rel="stylesheet" href="styles.css">            
                <link rel="icon" type="image/png" href="img/fav.png">
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
            </head>

            <body>

                <!-- I <3 Catherine!! -->
                
                <h2>Lawn Open-ness:</h2>

                <div id="uptime_heatmap"></div>

                <p align='center'>
                    Last updated {time_EST} Eastern.
                </p>

                <div id="back_button">
                    <a class="btn btn-primary btn-lg" href="index.html" role="button">Back</a>
                </div>

            </body>

        </html>
        """
    return vizgen_html
