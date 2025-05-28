from pydriller import Repository
from datetime import datetime
import subprocess
import csv
import os
import tempfile


java_files_directory = 'JavaFiles'  # name of the directory to save the files
if not os.path.exists(java_files_directory):  # create the directory if it doesn't exist
    os.makedirs(java_files_directory)



def get_readability_score(java_file):
    cmd = f"java -jar rsm.jar {java_file}"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    output_lines = result.stdout.splitlines()
    try:
        score = float(output_lines[-1].split('\t')[-1])
    except ValueError:
        score = 'not available'
    return score




# 2022-12-31

dt = datetime(2022, 12, 31, 23, 59, 0)
# for test
# dt = datetime(2023, 3, 15, 23, 59, 0)
# my_url = 'https://github.com/apache/commons-vfs'
# for test my_url = 'https://github.com/masoudsalehii/java'
files_list = [['file name','commit massage','commit hash','author name','committer date',
              'number of changed files for commit', 'old file path', 'new file path',
              'complexity', 'nloc','readability before commit','readability after commit', 'change in readability']]
list_of_java_files = []
# change the branch to main for test
#list_of_repo_urls = ['https://github.com/apache/commons-bcel', 'https://github.com/apache/commons-vfs', 'https://github.com/apache/commons-codec']
list_of_repo_urls = ['https://github.com/apache/commons-codec']
# list_of_repo_urls = ['https://github.com/masoudsalehii/java2']
name_of_columns = ['file name', 'commit msg', 'commit hash', 'author name', 'committer date', 'number of changed files',
                   'old path', 'new path', 'file complexity', 'nloc', 'readability before', 'readability current',
                   'difference']
for my_url in list_of_repo_urls:
    for commit in Repository(my_url, only_modifications_with_file_types=['.java'],
                             to=dt, only_in_branch='master').traverse_commits():
        for file in commit.modified_files:
            if file.source_code and file.source_code_before and file.filename.endswith(".java"):
                with open('info.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(name_of_columns)
                    row_of_csv = []
                    # file name
                    file_name = file.filename
                    row_of_csv.append(file_name)
                    # my_dict['file name'] = file_name
                    # commit message
                    commit_msg = commit.msg
                    row_of_csv.append(commit_msg)
                    # my_dict['commit massage'] = commit_msg
                    # commit hash
                    commit_hash = commit.hash
                    row_of_csv.append(commit_hash)
                    # my_dict['commit hash'] = commit_hash
                    # author name
                    author_name = commit.author.name
                    row_of_csv.append(author_name)
                    # my_dict['author name'] = author_name
                    # author email
                    # committer date
                    committer_dt = commit.committer_date
                    row_of_csv.append(committer_dt)
                    # number of changed files for each commit
                    # my_dict['committer date'] = committer_dt

                    # number if changed files
                    num_changed_files = commit.files
                    row_of_csv.append(num_changed_files)
                    # my_dict['number of changed files for commit'] = num_changed_files
                    # path for each file
                    # old path
                    file_old_path = file.old_path
                    row_of_csv.append(file_old_path)
                    # my_dict['old file path'] = file_old_path
                    # new path
                    file_new_path = file.new_path
                    row_of_csv.append(file_new_path)
                    # my_dict['new file path'] = file_new_path
                    # complexity for each file
                    file_complexity = file.complexity
                    row_of_csv.append(file_complexity)
                    # my_dict['complexity'] = file_complexity
                    # nloc for each file
                    file_nloc = file.nloc
                    row_of_csv.append(file_nloc)
                    # my_dict['nloc'] = file_nloc
                    # after version contents of the files
                    file_content_current = file.source_code
                    # print('current_' + file_name + '.java')
                    # with open('current_' + file_name , 'w') as java_file:
                    #         java_file.write(file_content_current)
                    #         list_of_java_files.append('current_' + file_name)
                    with open(os.path.join(java_files_directory, 'current_' + file_name), 'w') as java_file:
                        java_file.write(file_content_current)
                        # list_of_java_files.append(os.path.join(java_files_directory, 'current_' + file_name))
                    # my_dict['current file content'] = file_content_current
                    # before version contents of the files
                    file_content_before = file.source_code_before
                    # with open('before_'+file_name, 'w') as java_file:
                    #         java_file.write(file_content_before)
                    #         list_of_java_files.append('before_'+file_name)
                    with open(os.path.join(java_files_directory, 'before_' + file_name), 'w') as java_file:
                        java_file.write(file_content_before)
                        # list_of_java_files.append(os.path.join(java_files_directory, 'before_' + file_name))
                    # my_dict['before commit file content'] = file_content_before
                    # readability for each changed file
                    # readability before change
                    # readability after change
                    # print(os.path.join(java_files_directory, 'before_' + file_name))
                    val1 = get_readability_score(os.path.join(java_files_directory, 'before_' + file_name))
                    # print(os.path.join(java_files_directory, 'current_' + file_name))
                    val2 = get_readability_score(os.path.join(java_files_directory, 'current_' + file_name))
                    try:
                        diff = val2 - val1
                    except ValueError:
                        diff = 'not available'

                    row_of_csv.append(val1)
                    row_of_csv.append(val2)
                    row_of_csv.append(diff)
                    # files_list.append(row_of_csv)
                    if diff != 0 and diff != 'nan':
                        print(row_of_csv)
                    # files_list.append(row_of_csv)
                    # files_list.append(my_dict)
                    writer.writerow(row_of_csv)
                    print('loading')


