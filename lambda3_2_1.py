'''
3_2_1
'''
from bs4 import BeautifulSoup
import logging
import json

logging.basicConfig(filename="3_2_1.log", filemode='a')


# the code defines a custom FormatterJSON class that inherits from logging.Formatter. This class is responsible for formatting log records into JSON format.
class FormatterJSON(logging.Formatter):
    # Inside the FormatterJSON class, there's a format method. This method is called when a log record needs to be formatted.
    print("12")

    def format(self, record):
        # The record parameter represents a log record, containing information about the log event.
        print("15")
        # The format method begins by setting the message attribute of the log record by calling record.getMessage()
        record.message = record.getMessage()
        # The usesTime() method checks if the formatter should include time information in the log output.
        if self.usesTime():
            print("18")
            # If time information is included, the formatTime method is used to format the timestamp, and the result is assigned to record.asctime.
            record.asctime = self.formatTime(record, self.datefmt)
            # A payload dictionary is initialized with various pieces of information from the log record, such as levelname, time, aws_request_id, message, module, and rule_id.
        payload = {
            'levelname': record.levelname,
            'time': '%(asctime)s.%(msecs)dZ' % dict(asctime=record.asctime, msecs=record.msecs),
            'aws_request_id': getattr(record, 'aws_request_id', '00000000-0000-0000-0000-000000000000'),
            'message': record.message,
            'module': record.module,
            'rule_id': 'A_3.2.1'
        }
# If there's an exception associated with the log record (record.exc_info is not None),
        if record.exc_info:
            print("30")
            if not record.exc_text:  # the code checks whether record.exc_text is empty.
                print("32")
                # If it's empty, the code uses self.formatException to format the exception information and assigns it to record.exc_text.
                record.exc_text = self.formatException(record.exc_info)

        # If record.exc_text contains formatted exception information,
        if record.exc_text:
            print("36")
            # it's added to the payload dictionary.
            payload["exc_info"] = record.exc_text

        # if record.stack_info is present, stack_info(informative or useful information)
        if record.stack_info:
            print("40")
            # it's formatted and added to the payload dictionary under the key 'stack_info
            payload["stack_info"] = self.formatStack(record.stack_info)

        # The code then checks for extra data in the log record. ,
        extra_data = record.__dict__.get('data', {})
        print("extra_data 44", extra_data)
        if extra_data:  # If record.data is present
            print("46")
            # it's added to the payload dictionary under the key 'extras'.
            payload.update({
                'extras': extra_data
            })
# Finally, the json.dumps function is used to convert the payload dictionary into a JSON string. The default=str argument ensures that any non-serializable objects are converted to strings.
        return json.dumps(payload, default=str)


# The logger is obtained using logging.getLogger().
logger = logging.getLogger()
# The logger's level is set to 'INFO', which means that only log messages with a severity level of 'INFO' or higher will be processed by this logger.
logger.setLevel('INFO')
print("sneha")
# The FormatterJSON instance is created with a specified log message format and date format. This instance of the FormatterJSON class will be used to format log records. It appears that the format includes fields like levelname, asctime, msecs, levelno, and message.
formatter = FormatterJSON(
    '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
    '%Y-%m-%dT%H:%M:%S'
)
logger.handlers[0].setFormatter(formatter)


def modify_onfocus_atr(selector, value):
    print("65")
    new_json = {
        "type": "modify_atr",
        "data": {
            "selector": "",
            "atr": {
            }
        }
    }

    new_json['data']['selector'] = selector
    new_json['data']['atr'] = {"onfocus": value}

    return new_json


def modify_onclick_atr(selector, value):
    print("82")
    new_json = {
        "type": "modify_atr",
        "data": {
            "selector": "",
            "atr": {
            }
        }
    }

    new_json['data']['selector'] = selector
    new_json['data']['atr'] = {"onclick": value}

    return new_json


def lambda_handler(event, context):
    print("99")
    '''
    This rule is to check whether the change of context when input field receives focus
    '''
    logger.info(
        "Checking if their is a change of context when input field is on focus")
    datas = event
    final_data = {}
    try:
        print("try 108")
        logger.info("job_id:" + datas["jobId"])
    except:
        print("except 111")
        logger.warning("Request doesn't contain job_id, cannot process")
    try:
        print("try 114")
        soup = BeautifulSoup(datas['pageSource'], "html.parser")
        for key in datas:
            print("for 117")
            try:
                print("try 119")
                if key in ['pageSource', 'jobId']:
                    print("if 121")
                    # If the pagesource comes as key value, then we will omit it because as pagesource contains html scripts
                    continue
                # we are making action default to notify. If the logic found, we will change to 'fix' or nofixrequired
                datas[key]['action'] = 'notify'
                # For all the action cases editedcontext will occur,if the action is fix, editedcontext has some values for other case it will be  empty
                datas[key]["editedContext"] = ""
                try:
                    print("try 129")
                    # We are getting the context from the pagesource by using selector in the json
                    bs = soup.select_one(datas[key]['selector'])
                    print("bs", bs)
                    if bs is None:
                        print("if 133")
                        # If the selector cannot locate the context, then bs value will be none. So we are just notifying the case
                        datas[key]['action'] = 'unableToFix'
                        final_data[key] = datas[key]
                        continue
                except Exception as error_log:
                    print("except 139")
                    logger.error(f"{str(error_log)} unableToFix",
                                 exc_info=error_log)
                    # If the selector cannot locate the context
                    datas[key]['action'] = 'unableToFix'
                    final_data[key] = datas[key]
                    continue
                # we are assigning the context that come from beautifull soup to the json's context. As json context have incomplete contexts
                datas[key]['context'] = str(bs)
                if datas[key]['code'] == 'WCAG2AAA.Principle3.Guideline3_2.3_2_1.G107':
                    # Notifying the user by checking the cases
                    # If the onfocus attribute has this.focus or attribute is empty, no fix required4
                    # If the onclick attribute has this.focus or attribute is empty, no fix required
                    # If it doesn't meant any case, notify
                    # Checking for onfocus attribute
                    if bs.has_attr('onfocus'):
                        print("if 155")
                        if bs['onfocus'] == 'this.focus' or bs['onfocus'] == '':
                            print("if 157")
                            datas[key]['action'] = 'noFixRequired'
                        else:
                            print("else 160")
                            datas[key]['action'] = 'fix'
                            bs['onfocus'] = ''
                            datas[key]['editedContext'] = str(bs)
                            datas[key]["editedContextInJson"] = modify_onfocus_atr(
                                datas[key]['selector'], "")
                    # checking for onclick attribute
                    elif bs.has_attr('onclick'):
                        print("elif 168")
                        if bs['onclick'] == 'this.focus' or bs['onclick'] == '':
                            print("if 170")
                            datas[key]['action'] = 'noFixRequired'
                        else:
                            print("else 173")
                            datas[key]['action'] = 'fix'
                            bs['onclick'] = ''
                            datas[key]['editedContext'] = str(bs)
                            datas[key]["editedContextInJson"] = modify_onclick_atr(
                                datas[key]['selector'], "")
                    # the above case fails, so no focus element in the context so no fix required
                    else:
                        print("else 181")
                        datas[key]['action'] = 'noFixRequired'
                else:
                    print("else 184")
                    logger.info("Unable to process new code value!")
                    datas[key]['action'], datas[key]['editedContext'] = "notify", ""

            except Exception as error_log:
                print("except 189")
                logger.error(f"{str(error_log)} unableToFix",
                             exc_info=error_log)
                datas[key]['action'] = 'unableToFix'
                datas[key]["editedContext"] = ""
            final_data[key] = datas[key]
    except Exception as error_log:
        print("except 196")
        logger.error(f"{str(error_log)} unableToFix",
                     exc_info=error_log)
        datas[key]['action'] = 'unableToFix'
        datas[key]["editedContext"] = ""
        final_data[key] = datas[key]
    return final_data


with open('test_sample_1.json', 'r') as file:
    datas = json.load(file)
    final_data = lambda_handler(event=datas, context=None)
    final_json = json.dumps(final_data, indent=4)
    print(final_json)

# find sample for onclick with this.focus
