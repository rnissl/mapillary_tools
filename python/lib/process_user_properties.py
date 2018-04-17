import uuid

import lib.processor as processor
import lib.uploader as uploader


def finalize_user_properties_process(full_image_list, import_path, mapillary_description, verbose):
    for image in full_image_list:
        processor.create_and_log_process(
            image, import_path, mapillary_description, "user_process", verbose)


def process_user_properties(full_image_list, import_path, user_name, master_upload, verbose):
    mapillary_description = {}
    # if not master upload, user information has to be read from config file
    if not master_upload:
        try:
            mapillary_description = uploader.authenticate_user(
                user_name, import_path)
        except:
            print("Error, user authentication failed for user " + user_name)
            finalize_user_properties_process(
                full_image_list, import_path, {}, verbose)
            return
    else:
        try:
            master_key = uploader.get_master_key()
            if master_key:
                mapillary_description["MAPVideoSecure"] = master_key
                mapillary_description["MAPSettingsUsername"] = user_name
                try:
                    #user_key = uploader.get_user_key(user_name, master_key)
                    user_key = "test_key"
                    if user_key:
                        mapillary_description["MAPSettingsUserKey"] = user_key
                    else:
                        print("Error, no user key obtained for the user name " + user_name +
                              ", check if the user name is spelled correctly and if the master key is correct")
                        finalize_user_properties_process(
                            full_image_list, import_path, {}, verbose)
                        return
                except:
                    print("Error, no user key obtained for the user name " + user_name +
                          ", check if the user name is spelled correctly and if the master key is correct")
                    finalize_user_properties_process(
                        full_image_list, import_path, {}, verbose)
                    return
            else:
                print("Error, no master key found.")
                print("If you are a user, run the process script without the --master_upload, if you are a Mapillary employee, make sure you have the master key in your config file.")
                finalize_user_properties_process(
                    full_image_list, import_path, {}, verbose)
                return
        except:
            print("Error, no master key found.")
            print("If you are a user, run the process script without the --master_upload, if you are a Mapillary employee, make sure you have the master key in your config file.")
            finalize_user_properties_process(
                full_image_list, import_path, {}, verbose)
            return

    # a unique photo ID to check for duplicates in the backend in case the
    # image gets uploaded more than once
    mapillary_description['MAPPhotoUUID'] = str(uuid.uuid4())

    # create the json with the initial image description and log the user
    # properties process
    finalize_user_properties_process(
        full_image_list, import_path, mapillary_description, verbose)
