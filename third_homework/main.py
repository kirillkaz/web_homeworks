from jinja2 import Template, Environment, FileSystemLoader
from abc import ABC, abstractmethod, abstractproperty
from typing import Dict, Any, Tuple, List
import numpy as np

class Task(ABC):
    @abstractmethod
    def _get_template_html(self) -> Template:
        pass

    @abstractmethod
    def _get_context(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        pass 


class FirstTask(Task):
    def __init__(self, template_name: str):
        self.template_name = template_name

    def _get_template_html(self) -> Template:
        """Method for extraction template enviroment

        Returns:
            Template: template enviroment for work
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(self.template_name)

        return template

    def _get_context(self) -> Dict[str, Any]:
        """this method return context for jinja2

        Returns:
            Dict[int, str]: context for jinja2
        """
        name = 'colors'
        item_dict = {
            1: 'Красный',
            2: 'Зеленый',
            3: 'Синий',
        }

        key_list = [1, 2]

        context = {
            'name': name,
            'item_dict': item_dict,
            'key_list': key_list,
        }

        return context

    def execute(self, result_dir: str) -> None:
        """first task execution

        Args:
            result_dir (str): dir of file with result html
        """
        template = self._get_template_html()
        context = self._get_context()

        with open(result_dir, 'w', encoding='utf-8') as file:
            file.write(template.render(context))


class SecondTask(Task):
    def __init__(self, template_name: str, x_interval: Tuple[int, int], n_of_values: int):
        """constructor for second task

        Args:
            template_name (str): Dir of templates
            x_interval (Tuple[float, float]): Interval for table construction
            n_of_values (int): Count of values in interval
        """
        self._template_name = template_name
        self.x_list = x_interval
        self.n_of_values = n_of_values

    def _get_template_html(self) -> Template:
        """Method for extraction template enviroment

        Returns:
            Template: template enviroment for work
        """
        env = Environment(loader=FileSystemLoader('templates'))

        template = env.get_template(self._template_name)

        return template

    def _get_x_list(self) -> List[int]:
        """function which return list of x values on interval

        Returns:
            List[float]: list of x values
        """

        x_list = [i for i in range(self.x_list[0], self.x_list[1]+1)]
        return x_list

    def _get_funcs_results(self) -> Tuple[List[float], List[float]]:
        """method for calc funcs f(x), y(x), where:

        f(x) = (x-2)^2

        y(x) = (x-1)^3

        Returns:
            Tuple[List[float], List[float]]: tuple with lists of functions results, where
            
            first list - f(x)
            
            second list - y(x)
        """

        def f(x_list: List[float]) -> List[float]:
            """this function calc (x-2)^2

            Args:
                x_list (List[float]): list of values for calculation

            Returns:
                List[float]: list of values after calculation
            """
            return [(i-2)**2 for i in x_list]

        def y(x_list: List[float]) -> List[float]:
            """this function calc (x-1)^3

            Args:
                x_list (List[float]): list of values for calculation

            Returns:
                List[float]: list of values after calculation
            """
            return [(i-1)**3 for i in x_list]

        x_list = self._get_x_list()

        return f(x_list), y(x_list)

    def _get_context(self) -> Dict[str, Any]:
        """this method return context for jinja2

        Returns:
            Dict[int, str]: context for jinja2
        """

        x_list = self._get_x_list()

        funcs_results = self._get_funcs_results()

        item_dict = {
            'x': x_list,
            'f_x': funcs_results[0],
            'y_x': funcs_results[1],
        }

        context = {
            'item_dict': item_dict,
            'n': self.n_of_values
        }

        return context

    def execute(self, result_dir: str) -> None:
        """executor of the task2

        Args:
            result_dir (str): directory of the result html
        """
        template = self._get_template_html()
        context = self._get_context()

        with open(result_dir, 'w', encoding='utf-8') as file:
            file.write(template.render(context))


def main():
    first_task = FirstTask('source_task1.html')
    second_task = SecondTask('source_task2.html', [1,10], 5)
    # first_task.execute('templates/result.html')
    second_task.execute('templates/result.html')

if __name__ == "__main__":
    main()