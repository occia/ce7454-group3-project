# image processing related imports
import urllib.request as urllib
# import numpy as np
# import cv2
import json
import sys
import os

# image retrieval
def url_to_image(url):
    # image path
    
    # download the image by a URL
    resp = urllib.urlopen(url)
    # convert the image to a numpy array
    # image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # read the array into OpenCV 2D format with color encodings
	# image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return resp

def main(filename):
    
    country = 'Germany'
    users = 100
    img_path = '/home/polina/Desktop/data/Germany/images/'
    file_path = '/home/polina/Desktop/data/Germany/profiles/'

    # no-photo profile picture for comparison
    blank_url = 'https://instagram.fjed2-1.fna.fbcdn.net/vp/d116c35ad1dabd90ff3d0872a9d35074/5E41CEF1/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fjed2-1.fna.fbcdn.net'
    blank_photo = url_to_image(blank_url)

    parsed_users = []


#     head, tail = os.path.split(filename)
#     chunk = tail.split('.')[0]

    print('Parsing %s users of %s ', users, country)

    # profiles JSON parsing
    with open(filename, 'r') as file:
        user_profiles = json.load(file)
        for id, usr in enumerate(user_profiles[0:]):
            num = id
#             num = int(chunk) * 1000 + id
            # print('num is ' + str(num))
            url = usr['image']
            image_path = img_path + str(num) + '.jpg'
        # download the image URL
            if url != '':
                print ("downloading image")
                image = url_to_image(url)
#                 no_photo = np.array_equal(blank_photo,image)
                f = open(image_path,'wb')
                f.write(image.read())
                f.close()
#                 if not(no_photo):
#                     usr['parsed_image'] = num
#                     if usr['bio']:
#                         usr['is_valid'] = "Y"
#                     else:
#                         usr['is_valid'] = 'No Bio'
#                 elif usr['bio']:
#                     usr['parsed_image'] = 'N'
#                     usr['is_valid'] = 'No Photo'
#                 else: 
#                     usr['parsed_image'] = 'N'
#                     usr['is_valid'] = 'N'
#                 parsed_users.append(usr)
#                 np.save(image_path, image)

#     json_path = filepath + 'profiles.json'
#     # print(json_path + ' is json path')
#     with open(json_path, 'w') as outfile:
#         json.dump(parsed_users, outfile)

if __name__ == "__main__":
    # print(sys.argv[1])
    main(sys.argv[1])
