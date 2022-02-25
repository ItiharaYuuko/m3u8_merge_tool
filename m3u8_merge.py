from genericpath import isfile
from time import ctime
import os, shutil, threading
from os.path import isfile
from sys import argv
from posixpath import splitext
from cv2 import VideoCapture
from shutil import copy
def extension(f_name, index = -1):
    return splitext(f_name)[index].lower()
        
def get_ts_list(ext = '.ts'):
    return [i for i in os.listdir() if extension(i) == ext]

def get_duration(f_name):
    capl = VideoCapture(f_name)
    try:
        rate = capl.get(5)
        frame_num =capl.get(7)
        duration = frame_num/rate
        return duration
    except:
        return None

# def get_key_for_m3u8():
#     with open('kye0', 'rb+') as in_file:
#         rd_data = in_file.read()
#         return rd_data.hex()

# def process_files(key_insert):
#     fn_arr = []
#     or_arr = [i for i in os.listdir() if (len(i.split('.')) == 1) and (i.split('.')[0] != 'kye0')]
#     command_str = 'openssl aes-128-cbc -d -in %s -out %s -iv %s -K %s'
#     for f_n in or_arr:
#         tn = [j for j in re.findall('[0-9]*', f_n) if j.isdigit()][-1]
#         n_tn = 'n%05d' % int(tn)
#         fn_new = f_n.split('n')[0] + n_tn + '.ts'
#         fn_arr.append(fn_new)
#         if key_insert != '':
#             co_c = command_str % (f_n, fn_new, '0'*32, key_insert)
#             os.system(co_c)
#             print('[+]File %s was decryted.' % fn_new)
#         else:
#             shutil.copy(f_n, fn_new)
#             print('[+]File %s was copied.' % fn_new)

#     fn_arr.sort()
#     return fn_arr

def process_files(m3u8_name = argv[1]):
    fname_list = []
    with open(m3u8_name, 'r', encoding='utf-8') as m3_file:
        for line in m3_file.readlines():
            if not line.startswith('#'):
                tmp_fn = line.split('/')[-1].strip()
                if isfile(tmp_fn):
                    fname_list.append(tmp_fn)
    return fname_list

def sort_jud(i):
    return int(i.split('.')[0])

def merge_ts(array_insert):
    in_flist_name = '|'.join(array_insert)
    out_file_name = 'merged.mp4'
    index = 1 
    temp_str_arr = []
    part_ts_list = []
    f_count = 0
    comm_mme = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy %s'
    for inx in array_insert:
        if len(array_insert) > 10:
            temp_str_arr.append(inx)
            if index % 10 == 0:
                in_flist_name = '|'.join(temp_str_arr)
                out_file_name = '%s.ts' % f_count
                part_ts_list.append(out_file_name)
                comm_mme_part = comm_mme % (in_flist_name, out_file_name)
                os.system(comm_mme_part)
                f_count += 1
                temp_str_arr = []
            else:
                pass
            index += 1
            if index == int(len(array_insert)):
                in_flist_name = '|'.join(array_insert[f_count * 10:])
                out_file_name = '%s.ts' % f_count
                part_ts_list.append(out_file_name)
                comm_mme_part = comm_mme % (in_flist_name, out_file_name)
                os.system(comm_mme_part)
            else:
                pass
        else:
                in_flist_name = '|'.join(array_insert)
                out_file_name = '1.ts'
                part_ts_list.append(out_file_name)
                comm_mme_part = comm_mme % (in_flist_name, out_file_name)
                os.system(comm_mme_part)
                break
    comm_me = 'ffmpeg -i "concat:%s" -codec copy %s' % ('|'.join(part_ts_list), 'FinalMerged.mp4')
    print('[*]Merging files.')
    os.system(comm_me)
    print('[+]Files merged finished.')
    return part_ts_list

def clean_dir(array_insert):
    for dfn in array_insert:
        if os.path.isfile(dfn):
            os.remove(dfn)
            print('[-]File %s was removed.' % dfn)
        else:
            pass

def merge_main():
    sorted_f_li = []
    temp_purge_list = []
    # if os.path.exists('kye0'):
    #     keystr = get_key_for_m3u8()
    #     sorted_f_li = process_files(keystr)
    #     temp_purge_list = merge_ts(sorted_f_li)
    # else:
    sorted_f_li = process_files()
    temp_purge_list = merge_ts(sorted_f_li)

    clean_dir(sorted_f_li)
    clean_dir(temp_purge_list)
    print('[*]All Done.')

def copy_scripts_to_path(script_name):
    for dirx in [i for i in os.listdir() if os.path.isdir(i)]:
        shutil.copy(script_name, dirx + ('/%s' % script_name))
        print('%s -> %s Done.' % (script_name, dirx))

def process_path_merge():
    th_x = th_obj(merge_main, ())
    th_x.start()
    th_x.join()
    print('All done at %s' % ctime())

# def rename_path_videos():
#     mu_li = [j for j in os.listdir() if os.path.isfile(j) and (j.split('.')[-1] == 'm3u8')]
#     for m_name in mu_li:
#         for dirx in [i for i in os.listdir() if os.path.isdir(i)]:
#             if dirx in m_name:
#                 lv_name = m_name.split('_' + dirx)[0]
#                 os.chdir(dirx)
#                 nl_name = lv_name + '.mp4'
#                 while not os.path.isfile('FinalMerged.mp4'):
#                     pass
#                 os.rename('FinalMerged.mp4', nl_name)
#                 shutil.move(nl_name, '..')
#                 os.chdir('..')
#                 print('old name = %s, new name = %s' % ((dirx + '/' + 'FinalMerged.mp4'), nl_name))
#             else:
#                 pass

def video_no_duration_purge():
    for i in get_ts_list(ext = ''):
        if not get_duration(i):
            os.remove(i)
            

class th_obj(threading.Thread):
    def __init__(self, funx, args, t_name=''):
        threading.Thread.__init__(self)
        self.func = funx
        self.args = args
        self.name = t_name
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running  = threading.Event()
        self.__running.set()

    def get_result(self):
        return self.res

    def run(self, sig=1):
        self.res = ''
        index = 0
        while self.__running.isSet():
            self.__flag.wait()
            print('%s starting at %s.' % (self.func, ctime()))
            if sig > 0 and index < sig:
                self.res = self.func(*self.args)
            else:
                self.stop()
            print('%s terminated at %s.' % (self.func, ctime()))
            index += 1

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()

if __name__ == '__main__':
    #copy_scripts_to_path()
    video_no_duration_purge()
    process_path_merge()
    #rename_path_videos()
