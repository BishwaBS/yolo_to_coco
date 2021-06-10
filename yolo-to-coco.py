import os
import glob
import json

#Parameters
    # textfile_dir: The directory where all the text files for yolo are
    # output_dir: The directory where the coco json file is to be stored
    # file_name: The file name of the coco json file in <str> format. PLEASE PROVIDE FULL NAME INCLUDING .json extenstion. FOR EXAMPLE, myfile.json
    # img_extension: The extension of the images that are to be used for yolo training
    #img_width: Width of image
    #img_height: Height of image ##PLEASE NOTE THAT THIS SCRIPT WORKS ONLY WHEN ALL THE IMAGES ARE OF EQUAL SIZE
    #super_cat_name: The name of super category name . PLEASE REFER TO https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch FOR MORE DETAILS
    #Category names: A list of category names. For example, ["Bus", "Car", "Truck"]
    #info_dict: A dictionary for info on the dataset. PLEASE REFER TO https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch FOR MORE DETAILS

    # If license info is also,to be added, please pass the a dict containing license info in the line 38. for example, image["license"]= license_dict. the info and license dict are not
    # not importmant for analysis. So, analysis should run completely fine without them.

#Returns
    # coco json file

def yolo_to_coco(textfile_dir, output_dir, file_name, img_extension,  img_width, img_height, super_cat_name, category_names, info_dict=None):
    os.chdir(textfile_dir)

    #creating an empty dataframe
    data = {}
    data["info"] = []
    data["images"] = []
    data["annotations"] = []
    data["categories"] = []

    img_id=1
    #iterating over each text files
    for file in glob.glob("*" + ".txt"):
        with open(file, "r") as inputfile:

            #creating an empty image dictionary that stores image names and other info for each image corresponding to the text file iterated
            image = {}
            image["license"]=[]
            image["file_name"] = file.rsplit(".", 1)[0] + img_extension
            image["width"] = img_width
            image["height"] = img_height
            image["id"] = img_id
            print(image)
            data["images"].append(image)


            id=1
            #iterating over each line in the text file to extract annotation info and store in the annotation dictionary
            for line in inputfile:
                splits = line.split()
                x, y, w, h = float(splits[1]), float(splits[2]), float(splits[3]), float(splits[4])
                x1, y1 = int((x - w / 2) * image_width), int((y - h / 2) * image_height)
                x2, y2 = int((x + w / 2) * image_width), int((y + h / 2) * image_height)
                bbox= [x1, y1, abs(x2-x1), abs(y2-y1)]
                area = bbox[2]*bbox[3]
                categoryid= int(splits[0])+1


                annotation = {}
                annotation["id"] = id
                annotation["area"] = area
                annotation["bbox"] = bbox
                annotation["category_id"]=categoryid
                annotation["iscrowd"] = 0
                annotation["image_id"] = img_id


                print(annotation)
                data["annotations"].append(annotation)
                id += 1
        img_id += 1

    #Appending info_dict if passed
    if info_dict!=None:
        data["info"].append(info_dict)

    #Appending category names to the data dict
    for id, name in enumerate(category_names):
        data["categories"].append({
        "supercategory": super_cat_name,"id": id+1,"name": name})

    #exporting the "data" dict to json file
    def convert(o):
        if isinstance(o, np.generic): return o.item()
        raise TypeError

    with open(os.path.join(output_dir, file_name), "w") as file:
        json.dump(data, file, default=convert)

    return data


# yolo_to_coco("C:/Research", "C:/Research/output", "test_corn_GS2_cloudy_multi.json", ".JPG", 2048, 2048, "Weeds", ["MG", "Grass", "Other"])