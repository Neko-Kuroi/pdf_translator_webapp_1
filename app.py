import streamlit as st
import zipfile, shutil, time
import os
import hashlib
#from streamlit_pdf_viewer import pdf_viewer
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
#from streamlit_js_eval import streamlit_js_eval
import secrets
from pypdf import PdfReader
import glob

def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip


# colab side make dir
def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def main():

    if 'uniq' not in st.session_state:
        st.session_state.uniq = secrets.token_urlsafe()

    temp_dir = st.session_state.uniq
    my_makedirs(f"removefolder/{temp_dir}")

    flag = True
    if 'count' not in st.session_state:
        st.session_state.count = 0
    #tempolary
    if 'temp' not in st.session_state:
        st.session_state.temp = 0

    if 'lang' not in st.session_state:
        st.session_state.lang = ""
    if 'result' not in st.session_state:
        st.session_state.result = ""

    obj_0 = st.empty()
    obj_1 = st.empty()

    obj_0.header("`PDF file uploader`")
    st.markdown(f"The remote ip is `{get_remote_ip()}`")

    uploaded_file = obj_1.file_uploader("UPLOAD your .pdf file", type="pdf")
    ####
    if uploaded_file is not None:
        flag = False
        st.success("PDF file translator")
        # hashed
        raw_filename = uploaded_file.name
        intext_0 = f'<span style="color:LavenderBlush;background:Orchid">{raw_filename}</span>'
        st.write(intext_0, unsafe_allow_html=True)
        hashed_filename = hashlib.sha1(raw_filename.encode())
        uploadedfilename = hashed_filename.hexdigest()
        if "uploadedfilename" not in st.session_state:
            st.session_state.uploadedfilename = uploadedfilename

        if "book" not in st.session_state:
            #            pdf_viewer(input=uploaded_file.getvalue(), width=700, height=500)

            my_makedirs(
                f"removefolder/{temp_dir}/upload_folder_{st.session_state.count}"
            )

            with open(
                    f'removefolder/{temp_dir}/upload_folder_{st.session_state.count}/{uploadedfilename}.pdf',
                    'wb') as file:
                file.write(uploaded_file.getvalue())
#            pdf_viewer(input=f'{temp_dir}/upload_folder_{st.session_state.count}/{uploadedfilename}.pdf', width=700, height=500)

# read from PDF file
            PDF = glob.glob(
                f"removefolder/{temp_dir}/upload_folder_{st.session_state.count}/{uploadedfilename}.pdf"
            )

            doc = PdfReader(PDF[0])
            # meta = doc.metadata
            page_count = len(doc.pages)

            book = []  # PDF text data pool
            progressbar1 = st.empty()
            my_bar1 = progressbar1.progress(0)
            for index, page in enumerate(doc.pages):
                page_text = page.extract_text()
                book.append((index, page_text))
                done = int(((index + 1) / page_count) * 100)
                my_bar1.progress(done,
                                 text=f"Reading Page Number : {index + 1}")
            st.session_state.book = book
            my_bar1.empty()
            if os.path.isfile(
                    f"removefolder/{temp_dir}/upload_folder_{st.session_state.count}/{uploadedfilename}.pdf"
            ):
                shutil.rmtree(
                    f"removefolder/{temp_dir}/upload_folder_{st.session_state.count}/"
                )

        ########
        reload_bt = st.empty()
        if reload_bt.button("Upload another PDF file"):
            for key in st.session_state.keys():
                if key == "count" or key == "temp" or key == "lang":
                    continue
                else:
                    del st.session_state[key]
            shutil.rmtree(f"removefolder/{temp_dir}")
            # page reload
#            streamlit_js_eval(js_expressions="parent.window.location.reload()")
        st.markdown("----")

        plain_text1 = " 𓃠 select target language 𓃠 "
        var_text1 = f'##### <span style="color:green">{plain_text1}</span>'

        select = st.empty()
        select.write(var_text1, unsafe_allow_html=True)

        # select language
        st.markdown("""
        `ja`: **Japanese**,
        `en`: **English**,
        `fr`: **French**,
        `zb-TW`: **Chinese (traditional)**,
        `zh-CN`: **Chinese (simplified)**,
        `ru`: **Russian**,
        `ko`: **Korean**,
        `vi`: **Vietnamese**,
        `th`: **Thai**,
        `tl`: **Tagalog**,
        `ca`: **Catalan**,
        `si`: **Sinhalese**
        """)
        lang_code = [
            "select language",
            "Japanese",
            "English",
            "French",
            "Chinese traditional",
            "Chinese simplified",
            "Russian",
            "Korean",
            "Vietnamese",
            "Thai",
            "Tagalog",
            "Catalan",
            "Sinhalese",
        ]
        sel = st.empty()
        #language = sel.radio(
        #            label='translate to',
        #            options=lang_code,
        #            index=0,
        #            key = f"select_lang{st.session_state.count}")
        language = sel.selectbox(
            'translate to',
            lang_code,
            index=0,
            #placeholder = "select language",
            key=f"select_lang{st.session_state.count}")

        statename = f"select_lang{st.session_state.count}"
        if "target_lang" not in st.session_state:
            st.session_state.target_lang = "UNSELECTED"

        def reset_selected_lang():
            st.session_state[statename] = "select language"

        st.button('Reset Language', on_click=reset_selected_lang)

    area = st.empty()
    if flag:
        if "select_lang" in st.session_state:
            if st.session_state.select_lang != "select language":
                area2 = st.empty()
                plain_text2 = "☟Reset Language☟"
                empty_text = "☟              ☟"
                var_text2 = f'<span style="color:#FF69B4">{plain_text2}</span>'
                while flag:
                    area2.write(var_text2, unsafe_allow_html=True)
                    time.sleep(0.9)
                    area2.write(empty_text)
                    time.sleep(0.5)

        while flag:
            area.text("𓀤 upload PDF file 𓀤")
            time.sleep(1)
            area.text("𓀥                 𓀥")
            time.sleep(0.8)
    else:
        if f"select_lang{st.session_state.count}" in st.session_state:
            statename = f"select_lang{st.session_state.count}"
            if st.session_state[statename] != "select language":
                plain_text2 = "Reset Language"
                var_text2 = f'<span style="color:gray">▲ `{plain_text2}`</span>'
                area.write(var_text2, unsafe_allow_html=True)

        obj_0.empty()
        obj_1.empty()  # uploader hide

        # pdf translator
        #------------------------------------------
        st.markdown("----")
        st.success("translator")

        if "book" in st.session_state:
            book_data = st.session_state.book
            page_count = len(book_data)
        else:
            page_count = 0

        st.text(f"PDF total pages : {page_count}")

        progressbar = st.empty()
        my_bar = progressbar.progress(0)

        #3
        #        from google.colab import output
        import re
        #from googletrans import Translator
        from deep_translator import GoogleTranslator

        title_name = re.sub("\.| |%|@|\"|\'", "_", f"{uploaded_file.name}")

        if st.session_state.temp != int(st.session_state.count):
            st.session_state.lang = "init"
            st.session_state.temp = int(st.session_state.count)

        if language not in lang_code[1:]:
            language = None

        if st.session_state.lang != language and language is not None:
            st.session_state.count += 1
            st.session_state.result = ""
            st.session_state.lang = language

            my_makedirs(
                f"removefolder/{temp_dir}/work_{st.session_state.count}")

            to = ""
            match language:
                case "Japanese":
                    to = "ja"
                case "English":
                    to = "en"
                case "French":
                    to = "fr"
                case "Chinese traditional":
                    to = "zh-TW"
                case "Chinese simplified":
                    to = "zh-CN"
                case "Russian":
                    to = "ru"
                case "Korean":
                    to = "ko"
                case "Vietnamese":
                    to = "vi"
                case "Thai":
                    to = "th"
                case "Tagalog":
                    to = "tl"
                case "Catalan":
                    to = "ca"
                case "Sinhalese":
                    to = "si"
                case _:
                    to = "unknown"

            st.info(f"translate to [ {language} ]")

            st.session_state.target_lang = to

            work_area1 = st.empty()
            work_area2 = st.empty()
            #--------------------------------------

            for index, page in enumerate(book_data):
                page_text = page[1]
                #                print("\nPage Number:" + str(index))
                done = int(((index + 1) / page_count) * 100)
                my_bar.progress(done,
                                text=f"Working Page Number : {index + 1}")
                #  print(len(page_text))
                #  text_list = [s for s in page_text.split('\n') if s]
                page_text = re.sub('\.', '.𓂀', page_text)
                text_list = [s for s in page_text.split('𓂀')]
                if len(text_list) < 1:
                    continue

                limit = 0
                temp_list = []
                line_number = []

                for n, line in enumerate(text_list):
                    limit += 1
                    if limit > 10:
                        limit = 0


#                        output.clear()

                    line2 = re.sub(r"\s+", " ", line)
                    if line2 == "":
                        continue
                    temp_list.append((n, line2))

                    if len(temp_list) == 15 or n == len(text_list) - 1:
                        text_ = ""
                        all_text_orig = ""
                        all_text_done = ""
                        for i, t in enumerate(temp_list):
                            if t[1] != " ":
                                line_number.append(t[0])
                                text_ += '𓂀' + t[1].strip()
                        temp_list.clear()

                        text_2 = text_
                        text_ = re.sub('𓂀', "", text_)
                        while (re.search('𓂀', text_2)):
                            num = line_number.pop(0)
                            rep_words = f"𓃐NO:{num}| "
                            text_2 = text_2.replace('𓂀', rep_words, 1)
                        line_number.clear()

                        #                        print(re.sub("𓃐","\n", text_2))
                        #ts = Translator()
                        all_text_orig = f":::info\n𓃰{index + 1:05d}" + f"-{n}" + f";\n:::\n{text_}\n"

                        for times in range(0, 5):

                            try:
                                tsd = GoogleTranslator(
                                    source="auto",
                                    target=to).translate(text=text_)
                                if tsd == None:
                                    tsd = text_
                                #tsd = ts.translate(text_, src="en", dest="ja")
                                #translated_text = ts.translate(line, src="en", dest="ja").text
                                all_text_done = f":::info\n𓆏{index + 1:05d}" + f"-{n}" + f";\n:::\n{tsd}\n"
                                #all_text_done = f"**{index:05d}" + f"-{n}" + "; " +  tsd.text + "\n"

                                # all_text_orig += str(n) + "; " + tsd.pronunciation + "\n"
                                # print(index,n, line)
                                # print(index,n, tsd.text)

                                #                                print(all_text_orig)
                                #                                print(all_text_done + "\n")
                                if type(all_text_orig) is str and type(
                                        all_text_done) is str:

                                    #                                    intext_1 = f'<span style="color:DimGray;background:GhostWhite">{all_text_orig}</span>'
                                    #                                    work_area1.markdown(intext_1, unsafe_allow_html=True)
                                    work_area1.write(f"{all_text_orig}")
                                    # intext_2 = f'<span style="color:LavenderBlush;background:LightGray">{all_text_done}</span>'
                                    work_area2.write(f"{all_text_done}")
                                    # work_area2.markdown(intext_2, unsafe_allow_html=True)

                                    with open(
                                            f"removefolder/{temp_dir}/work_{st.session_state.count}/reuseMarkdown.txt",
                                            "a") as tempf:
                                        tempf.write(all_text_orig + "\n\n" +
                                                    all_text_done + "\n\n")

                                    # st.session_state.result += all_text_orig + "\n\n"
                                    # st.session_state.result += all_text_done + "\n\n"

                                # print(n, tsd.pronunciation)
                                with open(
                                        f"removefolder/{temp_dir}/work_{st.session_state.count}/{title_name}_done.txt",
                                        "a") as f:
                                    f.write(all_text_orig + all_text_done +
                                            "\n")
                                with open(
                                        f"removefolder/{temp_dir}/work_{st.session_state.count}/{title_name}_done_{language}.txt",
                                        "a") as f:
                                    f.write(all_text_done + "\n")

                                break

                            except Exception as e:
                                print(e)
                                time.sleep(3)
                                continue

                        with open(
                                f"removefolder/{temp_dir}/work_{st.session_state.count}/{title_name}_orig.txt",
                                "a") as f:
                            f.write(all_text_orig + "\n")

            
            st.markdown("----")

            my_makedirs(f"removefolder/{temp_dir}/download_section")
            shutil.move(
                f"removefolder/{temp_dir}/work_{st.session_state.count}/reuseMarkdown.txt",
                f"removefolder/{temp_dir}/download_section/reuseMarkdown_{st.session_state.count}.txt"
            )

            shutil.make_archive(
                f'removefolder/{temp_dir}/download_section/{st.session_state.uploadedfilename}_{st.session_state.count}',\
                format='zip',\
                root_dir=f'removefolder/{temp_dir}/work_{st.session_state.count}'\
                )
            shutil.rmtree(
                f"removefolder/{temp_dir}/work_{st.session_state.count}")

            st.balloons()
            work_area1.empty()
            work_area2.empty()
            
            #--------------------------------------

            st.success("Download translated text files")
            st.write(intext_0, unsafe_allow_html=True)
            # plain_text3 = f"[ {st.session_state.target_lang} ] : translated text files"
            plain_text3 = f"[ {language} ] : translated text files"
            var_text3 = f'##### <span style="color:#FF69B4">{plain_text3}</span>'

            translated = st.empty()
            translated.write(var_text3, unsafe_allow_html=True)

            if os.path.isfile(
                    f'removefolder/{temp_dir}/download_section/{st.session_state.uploadedfilename}_{st.session_state.count}.zip'
            ):
                with open(
                        f"removefolder/{temp_dir}/download_section/{st.session_state.uploadedfilename}_{st.session_state.count}.zip",
                        "rb") as fpath:
                    btn = st.download_button(
                        label=f"DOWNLOAD .zip file",
                        data=fpath,
                        file_name=
                        f"{st.session_state.uploadedfilename}_{st.session_state.count}.zip",
                        mime="application/zip")

            plain_text4 = "download zipfile"
            var_text4 = f'<span style="color:gray">▲ `{plain_text4}` 𓁉 </span>'
            st.write(var_text4, unsafe_allow_html=True)

            st.markdown("----")

            plain_text5 = " 𓀡 results 𓁙 "
            var_text5 = f'##### <span style="color:#20B2AA">{plain_text5}</span>'
            st.write(var_text5, unsafe_allow_html=True)

            tempf = open(
                f"removefolder/{temp_dir}/download_section/reuseMarkdown_{st.session_state.count}.txt"
            )
            all_result = tempf.read()
            tempf.close()
            st.write(intext_0, unsafe_allow_html=True)
            st.write(all_result, unsafe_allow_html=True)
            # st.write(st.session_state.result, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
