import requests
import json
import time
from bs4 import BeautifulSoup

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
}
# replace with the latest cookie
cookies = {
    "csrftoken": "",
    "sessionid": "",
    "cf_clearance": "",
}

url_list = [
    "https://study4.com/tests/toeic/?term=ETS%20(old%20format)",
    "https://study4.com/tests/toeic/?term=New%20economy",
    "https://study4.com/tests/toeic/?term=2018",
    "https://study4.com/tests/toeic/?term=2019",
    "https://study4.com/tests/toeic/?term=2020",
    "https://study4.com/tests/toeic/?term=2021",
    "https://study4.com/tests/toeic/?term=2022",
    "https://study4.com/tests/toeic/?term=2023",
    "https://study4.com/tests/toeic/?term=2024",
]


def crawl_exam_paper():
    try:
        exam_data = {}
        for url in url_list:
            response = requests.get(url, headers=headers, cookies=cookies, verify=False)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            test_items = soup.find_all("div", class_="col-6 col-md-3")
            url_temp = url.split("/")[-1]
            for test in test_items:
                href = test.find("a", class_="text-dark")["href"]
                temp_exam_title = href.split("/")[-2]
                exam_title = f"{url_temp}/{temp_exam_title}"
                exam_id = href.split("/")[2]
                exam_url = f"https://study4.com{href}"

                # get part 5 id.
                part_test_request = requests.get(
                    exam_url, headers=headers, cookies=cookies, verify=False
                )
                part_content = part_test_request.text
                part_soup = BeautifulSoup(part_content, "html.parser")
                div = part_soup.find("div", id="test-solutions")
                list_items = div.find_all("li")
                href_part5 = None
                for li in list_items:
                    span = li.find("span")
                    if span and "Part 5" in span.text:
                        a_tag = li.find("a")
                        if a_tag:
                            href_part5 = a_tag["href"]
                        break
                transcript_url = f"https://study4.com{href_part5}"
                part5_id = href_part5.split("/")[-3]
                question_url = (
                    f"https://study4.com/tests/{exam_id}/practice/?part={part5_id}"
                )
                exam_data[exam_title] = {
                    "questions": question_url,
                    "transcript": transcript_url,
                }

        json_object = json.dumps(exam_data, indent=4)
        with open("./data_exam_paper_url.json", "w") as jf:
            jf.write(json_object)
    except Exception as e:
        print(f"Got an error: {str(e)}")


def crawl_exam_data():
    try:
        with open("./data_exam_paper_url.json", "r") as file_url:
            dict_url_data = json.load(file_url)

        previous_key = ""
        count = 0
        total_question = {}

        for k, v in dict_url_data.items():

            response_transcript = requests.get(
                v["transcript"], headers=headers, cookies=cookies, verify=False
            )
            transcript_content = response_transcript.text

            transcript_soup = BeautifulSoup(transcript_content, "html.parser")
            transcript_wrapper = transcript_soup.find_all(
                "div", class_="question-wrapper"
            )

            transcript_data = {}
            for question in transcript_wrapper:
                result_text = question.find("div", class_="mt-2 text-success").get_text(
                    strip=True
                )
                final_result = result_text.split(":")[-1]
                result_data = {
                    "result_number": question.find("strong").get_text(strip=True),
                    "result_text": final_result,
                }
                transcript_data[result_data["result_number"]] = result_data

            time.sleep(5)
            response = requests.get(
                v["questions"], headers=headers, cookies=cookies, verify=False
            )
            questions_term = {}
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            list_question_wrapper = soup.find_all("div", class_="question-wrapper")
            for question_wrapper in list_question_wrapper:
                question_number = question_wrapper.find(
                    "div", class_="question-number"
                ).strong.get_text(strip=True)
                question_data = {
                    "question_number": question_number,
                    "question_text": question_wrapper.find(
                        "div", class_="question-text"
                    ).get_text(strip=True),
                    "transcript": transcript_data[question_number].get("result_text"),
                    "answers": [],
                }
                answers = question_wrapper.find_all("div", class_="form-check")
                for answer in answers:
                    answer_text = answer.label.get_text(strip=True)
                    question_data["answers"].append(answer_text)
                questions_term[question_data["question_number"]] = question_data
            current_key = k.split("/")[0]
            if not previous_key or current_key == previous_key:
                total_question[k] = questions_term
            else:
                count += 1
                json_object = json.dumps(total_question, indent=4)
                with open(f"../data/questions_{count}.json", "a") as fw:
                    fw.write(json_object)
                total_question = {}
                total_question[k] = questions_term

            previous_key = k.split("/")[0]
            time.sleep(5)

        count += 1
        json_object = json.dumps(total_question, indent=4)
        with open(f"../data/questions_{count}.json", "a") as fw:
            fw.write(json_object)
        total_question = {}
    except Exception as e:
        print(f"Got an error: {str(e)}")


# first start crawl_exam_paper , then crawl_exam_data.
crawl_exam_paper()
crawl_exam_data()
