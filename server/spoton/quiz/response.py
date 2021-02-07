import logging
import types

from spoton.models.quiz import *
from spoton.models.response import *

logger = logging.getLogger(__name__)


def save_response(data):
    """Processes a user's response to the quiz and saves it to the db.

    Processes a user's response to the quiz, loads their answers into
    Response object, and saves it to the database.

    Parameters
    ----------
    data : dict
        A JSON dictionary of the user's response data. Format specified
        in coord/response.json (above the server folder). 
    
    Returns
    -------
    bool
        True if the response was processed and saved successfully,
        False otherwise.
    """

    #import pprint; pprint.pprint(data)

    # Find the specified quiz
    quizzes = Quiz.objects.filter(user_id=data.get('quiz_id'))
    if not quizzes:
        logger.error('Processing Response: No quiz was found with id '
                + str(data.get('quiz_id')) + '. This is an internal error.')
        return False

    quiz = quizzes[0]



    # Load in general response data and create response object
    name = data.get('name')
    # emoji
    # background color

    response = Response.objects.create(quiz=quiz, name=name)



    # Process each question response
    for q in data.get('questions'):

        # Get answer(s) for the specific question
        answers = q.get('answer')
        if not answers:
            response.delete()
            logger.error('Processing Response: No answer found for question '
                    + str(q) + '. This is an internal error.')
            return False


        # If there's a list of answers (even only one), it's a checkbox
        # question
        if(type(answers) is list):

            # Get the specified question object
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


            # Go through each of the answers and load the associated
            # Choice object
            for a in answers:
                c = Choice.objects.filter(id=a)
                if not c:
                    response.delete()
                    logger.error('Processing Response: No Choice object '
                            + 'found with id ' + str(a) +
                            '. This is an internal error.')
                    return False

                try:
                    qr.choices.add(c[0])
                except ValidationError as e:
                    response.delete()
                    logger.error(e)
                    logger.error('ValidationError raised when adding '
                            + 'Choice to CheckboxResponse. This is an '
                            + 'internal error.')
                    return False
            
        # Slider question
        else:
            # Get the specified question object
            questions = SliderQuestion.objects.filter(id=q.get('question_id'))
            if not questions:
                response.delete()
                logger.error('Processing Response: No SliderQuestion found '
                        + 'for question ' + str(q) +
                        '. Are you sure the answers should not be a list? '
                        + 'This is an internal error.')
                return False
            question = questions[0]


            qr = SliderResponse.objects.create(response=response,
                    question=question, answer=answers)


    return True 
