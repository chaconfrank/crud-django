import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently return False for question whose pub_date is in the future """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='¿Quien es el mejor CD de plazi?', pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)


class QuestionIndexViewTest(TestCase):

    def create_question(self, question_text, days):
        """
        Create a question with the given "question_text", and published the given
        number of days offset to now (negative for question published in the past,
        positive for question that have yet to be published)
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

    def test_no_question(self):
        """If not question exists, an appropiate message is displayed"""

        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_future_question(self):
        """
        Check if question model has a question in the future and it musnt show any question
        """

        self.create_question('Future question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_past_question(self):
        """
        Question with pub_date in the past are displayed on the index.
        """
        question = self.create_question('Past question', -10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past question are displayed
        """

        past_question = self.create_question(question_text='Past question', days=-30)
        future_question = self.create_question(question_text='Future question', days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['lastest_question_list'], [past_question]
        )

    def test_two_past_question(self):
        """
        The question index page may display multiple questions
        """

        past_question_1 = self.create_question(question_text='Past question 1', days=-30)
        past_question_2 = self.create_question(question_text='Past question 2', days=-40)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['lastest_question_list']
                                 , [past_question_1, past_question_2])

    def test_two_future_question(self):
        """
        Even if I have two questions future the index view it will show the message 'No polls are available.'
        """

        future_question_1 = self.create_question(question_text='Future question 1', days=30)
        future_question_2 = self.create_question(question_text='Future question 2', days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])


class QuestionDetailViewTest(TestCase):

    def create_question(self, question_text, days):
        """
        Create a question with the given "question_text", and published the given
        number of days offset to now (negative for question published in the past,
        positive for question that have yet to be published)
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

    def test_future_question(self):
        """
        The detail view of a question with pub_date in the future return a 404 error not found
        """
        future_question_1 = self.create_question(question_text='Future question 1', days=30)
        url = reverse('polls:detail', args=(future_question_1.id, ))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with pub_date in the past displays the question's text
        """
        past_question = self.create_question(question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
