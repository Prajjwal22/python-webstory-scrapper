from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import html

app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, From Lambda!</p>"

@app.route('/process_web_story', methods=['GET', 'POST'])
def process_web_story():
    title = ""  # Initialize title with an empty string
    if request.method == 'POST':
        print(request)
        # Get the web story URL from the frontend
        web_story_url = request.json.get('web_story_url')

        # Replace with the URL of the AMP web story
        # web_story_url = "https://www.hindustantimes.com/web-stories/in-focus/pm-modis-memorable-sortie-on-tejas-fighter-jet-101700909742660.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        print("request made")
        # Send an HTTP GET request to the web story
        response = requests.get(web_story_url, headers=headers)

        # Your WordPress username
        username = 'stupefied-bassi'

        # The application password you generated
        password = '4GG5 Spro I3Z4 72dk jBks 12VB'

        image_ids = []

        def upload_images(image_url,text):

        # Download the image from the remote URL
            image_response = requests.get(image_url, headers=headers)
            if image_response.status_code == 200:
                image_data = image_response.content
                file_name = f"{text}.jpg"

                # Upload image to WordPress
                upload_url = f"https://apis.newsbust.in/wp-json/wp/v2/media"
                files = {'file': (file_name, image_data)}
                upload_response = requests.post(upload_url, headers=headers,auth=(username, password), files=files)

                if upload_response.status_code == 201:
                    uploaded_image_url = upload_response.json().get('source_url')
                    image_ids.append(upload_response.json().get('id'))
                    print("Image uploaded successfully. URL:", uploaded_image_url)
                    return uploaded_image_url
                else:
                    print("Image upload failed.")
            else:
                print("Failed to download the remote image.")

        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the slides within the web story
            slide_elements = soup.find_all('amp-story-page')
            title = soup.find('title').get_text()

            # Create a list to store slide objects
            slides = []
            amp_story_pages = ''
            # Define text outside the loop
            text = None
            json_script = [
            {
                "selector": "#anim-cd2d422d-9a67-4cf7-8baa-b4fb6085a167",
                "keyframes": {"transform": ["translate(0%, 0%) scale(1.5)", "translate(0%, 0%) scale(1)"]},
                "delay": 0,
                "duration": 7000,
                "easing": "cubic-bezier(.3,0,.55,1)",
                "fill": "forwards"
            }
            ]
            json_string = json.dumps(json_script)

            poster_image = slide_elements[0].find('amp-story-grid-layer').find('amp-img')['src']
            publisher_logo = "https://newsbust.in/icon.png"
            for slide_index, slide in enumerate(slide_elements):
                # Extract text from the slide
                text_elements = slide.find(['h2', 'h1'])
                if text_elements:
                    for text_element in text_elements:
                        text = text_element.get_text()
                        print(text)

                # Find and extract the image URL from the slide background
                image_element = slide.find('amp-story-grid-layer').find('amp-img')
                if image_element:
                    image_url = upload_images(image_element['src'],text)
                else:
                    print("No image found for this slide")
                    image_url = None

                # Create a dictionary object for the current slide

                amp_story_page_template = f'''
                        <amp-story-page id="{slide_index}" auto-advance-after="7s">
                    <amp-story-animation layout="nodisplay" trigger="visibility">
                        <script
                        type="application/json">{json_string}</script>
                    </amp-story-animation><amp-story-grid-layer template="vertical" aspect-ratio="412:618" class="grid-layer">
                        <div class="page-fullbleed-area" style="background-color:#f3f3f3">
                            <div class="page-safe-area">
                                <div
                                    style="position:absolute;pointer-events:none;left:0;top:-9.25926%;width:100%;height:118.51852%;opacity:1">
                                    <div id="anim-cd2d422d-9a67-4cf7-8baa-b4fb6085a167" class="animation-wrapper"
                                        style="width:100%;height:100%;display:block;position:absolute;top:0;left:0">
                                        <div style="pointer-events:initial;width:100%;height:100%;display:block;position:absolute;top:0;left:0;z-index:0"
                                            class="mask" id="el-1">
                                            <div style="position:absolute;width:118.51852%;height:100%;left:-9.25926%;top:0%"
                                                data-leaf-element="true"><amp-img layout="fill"
                                                    src="{image_url}"
                                                    alt="{text}"></amp-img></div>
                                            <div class="element-overlay-area"
                                                style="background-image:linear-gradient(0.5turn, rgba(0,0,0,0) 71%, rgba(0,0,0,0.7) 100%)">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="page-background-overlay-area"
                                    style="background-image:linear-gradient(0.5turn, rgba(0,0,0,0) 71%, rgba(0,0,0,0.7) 100%)">
                                </div>
                            </div>
                        </div>
                    </amp-story-grid-layer><amp-story-grid-layer template="vertical" aspect-ratio="412:618" class="grid-layer">
                        <div class="page-fullbleed-area">
                            <div class="page-safe-area">
                                <div
                                    style="position:absolute;pointer-events:none;left:11.40777%;top:74.43366%;width:76.94175%;height:27.50809%;opacity:1">
                                    <div style="pointer-events:initial;width:100%;height:100%;display:block;position:absolute;top:0;left:0;z-index:0;border-radius:0.6309148264984227% 0.6309148264984227% 0.6309148264984227% 0.6309148264984227% / 1.1764705882352942% 1.1764705882352942% 1.1764705882352942% 1.1764705882352942%"
                                        id="el-6">
                                        <p class="fill text-wrapper"
                                            style="white-space:pre-line;overflow-wrap:break-word;word-break:break-word;margin:0.5488958990536283% 0;font-family:&quot;Nunito&quot;,sans-serif;font-size:0.323625em;line-height:1.19;text-align:center;padding:0;color:#000000">
                                            <span style="color: #fff">{text}</span></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </amp-story-grid-layer>
                </amp-story-page>'''

                amp_story_pages += amp_story_page_template

                slide_data = {
                    "elements": [
                        {
                            "opacity": 100,
                            "flip": {"vertical": False, "horizontal": False},
                            "rotationAngle": 0,
                            "lockAspectRatio": True,
                            "scale": 100,
                            "focalX": 50,
                            "focalY": 50,
                            "resource": {
                                "type": "image",
                                "mimeType": "image/jpeg",
                                "width": 4160,
                                "height": 6240,
                                "isPlaceholder": False,
                                "isExternal": True,
                                "needsProxy": False,
                                "id": f"media/{slide_index + 1}",  # Adjust the ID as needed
                                "baseColor": "#f3f3f3",
                                "blurHash": "LkKnxZoeVsaJ_NWVf6RjkrWBayWB",
                                "creationDate": "2023-11-08T07:22:56Z",
                                "src": image_url,
                                "alt": f"Slide {slide_index + 1}",
                            },
                            "backgroundColor": {"color": {"r": 196, "g": 196, "b": 196}},
                            "x": 48,
                            "y": 0,
                            "width": 330,
                            "height": 494,
                            "mask": {"type": "rectangle"},
                            "isBackground": True,
                            "id": f"{slide_index + 1}",
                            "overlay": {
                                "type": "linear",
                                "stops": [
                                    {"color": {"r": 0, "g": 0, "b": 0, "a": 0}, "position": 0.71},
                                    {"color": {"r": 0, "g": 0, "b": 0}, "position": 1},
                                ],
                                "alpha": 0.7,
                            },
                            "type": "image",
                        },
                        {
                            "opacity": 100,
                            "flip": {"vertical": False, "horizontal": False},
                            "rotationAngle": 0,
                            "lockAspectRatio": True,
                            "backgroundTextMode": "NONE",
                            "font": {"family": "Nunito"},
                            "fontSize": 24,
                            "backgroundColor": {"color": {"r": 196, "g": 196, "b": 196}},
                            "lineHeight": 1.19,
                            "textAlign": "center",
                            "padding": {
                                "locked": True,
                                "hasHiddenPadding": False,
                                "horizontal": 0,
                                "vertical": 0,
                            },
                            "content": f'<span style=\"color: #ffffff\">{text}</span>',
                            "x": 46,
                            "y": 550,
                            "width": 318,
                            "borderRadius": {
                                "locked": True,
                                "topLeft": 2,
                                "topRight": 2,
                                "bottomRight": 2,
                                "bottomLeft": 2,
                            },
                            "height": 61,
                            "id": f"{slide_index + 2}",  # Adjust the ID as needed
                            "marginOffset": -4.35,
                            "type": "text",
                        },
                    ],
                    "backgroundColor": {"color": {"r": 255, "g": 255, "b": 255}},
                    "animations": [
                        {
                            "id": f"effect-background-zoom-{slide_index + 1}",
                            "type": "effect-background-zoom",
                            "zoomDirection": "scaleOut",
                            "duration": 7000,
                            "delay": 0,
                            "targets": [f"{slide_index + 1}"],
                        }
                    ],
                    "id": f"{slide_index + 3}",  # Adjust the ID as needed
                    "defaultBackgroundElement": {
                        "opacity": 100,
                        "flip": {"vertical": False, "horizontal": False},
                        "rotationAngle": 0,
                        "lockAspectRatio": True,
                        "backgroundColor": {"color": {"r": 196, "g": 196, "b": 196}},
                        "x": 1,
                        "y": 1,
                        "width": 1,
                        "height": 1,
                        "mask": {"type": "rectangle"},
                        "isBackground": True,
                        "isDefaultBackground": True,
                        "type": "shape",
                        "id": f"{slide_index + 4}",  # Adjust the ID as needed
                    },
                }

                # Append the slide data to the list of slides
                slides.append(slide_data)

            amp_html_format = f''' <html amp="" lang="en">

        <head>
            <meta charSet="utf-8" />
            <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1" />
            <script async="" src="https://cdn.ampproject.org/v0.js"></script>
            <script async="" src="https://cdn.ampproject.org/v0/amp-story-1.0.js" custom-element="amp-story"></script>
            <link href="https://fonts.googleapis.com/css2?display=swap&amp;family=Nunito" rel="stylesheet" />
            <style amp-boilerplate="">
                body {{
                    -webkit-animation: -amp-start 8s steps(1, end) 0s 1 normal both;
                    -moz-animation: -amp-start 8s steps(1, end) 0s 1 normal both;
                    -ms-animation: -amp-start 8s steps(1, end) 0s 1 normal both;
                    animation: -amp-start 8s steps(1, end) 0s 1 normal both
                }}

                @-webkit-keyframes -amp-start {{
                    from {{
                        visibility: hidden
                    }}

                    to {{
                        visibility: visible
                    }}
                }}

                @-moz-keyframes -amp-start {{
                    from {{
                        visibility: hidden
                    }}

                    to {{
                        visibility: visible
                    }}
                }}

                @-ms-keyframes -amp-start {{
                    from {{
                        visibility: hidden
                    }}

                    to {{
                        visibility: visible
                    }}
                }}

                @-o-keyframes -amp-start {{
                    from {{
                        visibility: hidden
                    }}

                    to {{
                        visibility: visible
                    }}
                }}

                @keyframes -amp-start {{
                    from {{
                        visibility: hidden
                    }}

                    to {{
                        visibility: visible
                    }}
                }}
            </style><noscript>
                <style amp-boilerplate="">
                    body {{
                        -webkit-animation: none;
                        -moz-animation: none;
                        -ms-animation: none;
                        animation: none
                    }}
                </style>
            </noscript>
            <style amp-custom="">
                h1,
                h2,
                h3 {{
                    font-weight: normal;
                    color:#ffffff;
                    padding:9px 5px;
                }}

                amp-story-page {{
                    background-color: #131516;
                }}

                amp-story-grid-layer {{
                    overflow: visible;
                }}

                @media (max-aspect-ratio: 9 / 16) {{
                    @media (min-aspect-ratio: 320 / 678) {{
                        amp-story-grid-layer.grid-layer {{
                            margin-top: calc((100% / 0.5625 - 100% / 0.6666666666666666) / 2);
                        }}
                    }}
                }}

                @media not all and (min-resolution:.001dpcm) {{
                    @media {{
                        p.text-wrapper>span {{
                            font-size: calc(100% - 0.5px);
                        }}
                    }}
                }}

                .page-fullbleed-area,
                .page-background-overlay-area {{
                    position: absolute;
                    overflow: hidden;
                    width: 100%;
                    left: 0;
                    height: calc(1.1851851851851851 * 100%);
                    top: calc((1 - 1.1851851851851851) * 100% / 2);
                }}

                .element-overlay-area {{
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                }}

                .page-safe-area {{
                    overflow: visible;
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    width: 100%;
                    height: calc(0.84375 * 100%);
                    margin: auto 0;
                }}

                .mask {{
                    position: absolute;
                    overflow: hidden;
                }}

                .fill {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    margin: 0;
                }}

                @media (prefers-reduced-motion: no-preference) {{
                    .animation-wrapper {{
                        opacity: var(--initial-opacity);
                        transform: var(--initial-transform);
                    }}
                }}

                amp-story-grid-layer.align-bottom {{
                    align-content: end;
                    padding: 0;
                }}

                .captions-area {{
                    padding: 0 32px 0;
                }}

                amp-story-captions {{
                    margin-bottom: 16px;
                    text-align: center;
                }}

                amp-story-captions span {{
                    display: inline-block;
                    margin: 0;
                    padding: 6px 12px;
                    vertical-align: middle;
                    border-radius: 15px;
                    background: rgba(11, 11, 11, 0.6);
                    color: rgba(255, 255, 255, 1);
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
                    ;
                    font-size: calc(4 * var(--story-page-vw));
                    line-height: 1.4;
                    word-break: break-word;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                }}

                span{{
                        color: white;
                padding: 8px 5px;
                position: absolute;
                z-index: 9999;
                bottom: 0;
                    background-color: #00000024;
                    left: 0;
                }}

                amp-img img {{
                object-fit:cover
                }}
            </style>
            <meta name="web-stories-replace-head-start" />
            <title>{title}</title>
            <link rel="canonical" href="https://newsbust.in/web-stories/huma-qureshis-iconic-ethnic-look/" />
            <meta name="web-stories-replace-head-end" />
        </head>

        <body><amp-story standalone="" publisher="newsbust.in" publisher-logo-src="{publisher_logo}"
                title="{title}" poster-portrait-src="{poster_image}">

            {amp_story_pages}
                </amp-story></body>

        </html> '''

            format = {
        "version": 47,


        "fonts": {
            "Nunito": {
            "family": "Nunito",
            "fallbacks": ["sans-serif"],
            "weights": [200, 300, 400, 500, 600, 700, 800, 900],
            "styles": ["regular", "italic"],
            "variants": [
                [0, 200],
                [0, 300],
                [0, 400],
                [0, 500],
                [0, 600],
                [0, 700],
                [0, 800],
                [0, 900],
                [1, 200],
                [1, 300],
                [1, 400],
                [1, 500],
                [1, 600],
                [1, 700],
                [1, 800],
                [1, 900]
            ],
            "service": "fonts.google.com",
            "metrics": {
                "upm": 1000,
                "asc": 1011,
                "des": -353,
                "tAsc": 1011,
                "tDes": -353,
                "tLGap": 0,
                "wAsc": 1077,
                "wDes": 300,
                "xH": 484,
                "capH": 705,
                "yMin": -276,
                "yMax": 1039,
                "hAsc": 1011,
                "hDes": -353,
                "lGap": 0
            }
            }
        },
        "autoAdvance": True,
        "defaultPageDuration": 7,
        "currentStoryStyles": { "colors": [] },
        "pages":slides

        }

            # ampHTML = ampHTML_template.format(title=html.escape(title))

            # print(amp_html_format)
            print(image_ids)



            # Convert the list of slides to a JSON-formatted string
            json_data = json.dumps(format, indent=2)
            json_data_escaped = json_data.replace('<span style="', '<span style=\\"').replace('">', '\\">')

            # Print or save the JSON data
            # print(json_data)

        else:
            print(f"Failed to retrieve the web story. Status code: {response.status_code}")

    if title:
        # The URL for the API endpoint
        url = 'https://apis.newsbust.in/wp-json/wp/v2/web-stories'

        # The post data
        data = {
            'title': title,
            'content': json_data_escaped,
            'status': 'publish',  # Use 'draft' to save the post as a draft
            'html_content': amp_html_format,
            'poster_image_url':poster_image,
            'poster_image':image_ids[0]
        }

        # Send the HTTP request
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, auth=(username, password), json=data, headers=headers)

        # Check the response
        if response.status_code == 200:
            print('Post created successfully')
        else:
            print('Failed to create post: ' + response.text)
        
        # Replace the print statements with a dictionary containing necessary information
        result = {
            "message": "Processing completed" + image_ids,
            # Add any relevant data you want to send back to the frontend
        }
        return jsonify(result), 200
    else:
        return jsonify({"error": "Invalid reqbhbhest method"}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
