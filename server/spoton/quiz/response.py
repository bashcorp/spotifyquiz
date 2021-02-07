import logging
import types

from spoton.models.quiz import *
from spoton.models.response import *

logger = logging.getLogger(__name__)


def save_response(data):

    #import pprint; pprint.pprint(data)

    quizzes = Quiz.objects.filter(user_id=data.get('quiz_id'))
    if not quizzes:
        logger.error('Processing Response: No quiz was found with id '
                + str(data.get('quiz_id')) + '. This is an internal error.')
        return False

    quiz = quizzes[0]

    name = data.get('name')

    response = Response.objects.create(quiz=quiz, name=name)

    for q in data.get('questions'):

        answers = q.get('answer')

        if not answers:
            response.delete()
            logger.error('Processing Response: No answer found for question '
                    + str(q) + '. This is an internal error.')
            return False


        if(type(answers) is list):
            questions = CheckboxQuestion.objects.filter(id=q.get('question_id'))
            if not questions:
                response.delete()
                logger.error('Processing Response: No CheckboxQuestion found '
                        + 'for question ' + str(q) +
                        '. This is an internal error.')
                return False

            question = questions[0]

            qr = CheckboxResponse.objects.create(response=response,
                    question=question)

            for a in answers:
                c = Choice.objects.filter(id=a)
                if not c:
                    response.delete()
                    logger.error('Processing Response: No Choice object '
                            + 'found for answer ' + str(a) +
                            '. This is an internal error.')
                    return False
                qr.choices.add(c[0])
            
        else:
            questions = SliderQuestion.objects.filter(id=q.get('question_id'))
            if not questions:
                response.delete()
                logger.error('Processing Response: No SliderQuestion found '
                        + 'for question ' + str(q) +
                        '. Are you sure the answers should not be a list. '
                        + 'This is an internal error.')
                return False

            question = questions[0]

            qr = SliderResponse.objects.create(response=response,
                    question=question, answer=answers)


    return True 
