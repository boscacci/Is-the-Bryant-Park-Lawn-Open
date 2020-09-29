def generate_vizgen_html(time_EST, n_weeks):
    print("Generating stats page HTML...")
    vizgen_html = f"""
        <!doctype html>
        <html lang="en">

            <head>
                <title>Is the Bryant Park Lawn Open Stats</title>
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
                
                <div class="centered">
                    <h2 id="openness">Average Lawn Openness (Mean)</h2>    
                </div>

                <div id="uptime_heatmap"></div>

                <p align='center'>
                    This represents ~{n_weeks} weeks of twice-hourly sampling.
                </p>

                <p align='center'>
                    Last updated {time_EST} Eastern.
                </p>

                <div id="back_button" class="centered">
                    <a class="btn btn-primary btn-lg" href="index.html" role="button">Back</a>
                </div>

            </body>

        </html>
        """
    return vizgen_html
