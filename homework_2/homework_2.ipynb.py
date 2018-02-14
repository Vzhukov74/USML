{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "<img src=\"../../img/ods_stickers.jpg\">\n",
    "## Открытый курс по машинному обучению. Сессия № 2\n",
    "Автор материала: Илья Барышников (@lucidyan). Материал распространяется на условиях лицензии [Creative Commons CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Можно использовать в любых целях (редактировать, поправлять и брать за основу), кроме коммерческих, но с обязательным упоминанием автора материала."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# <center> Домашнее задание №2\n",
    "## <center> Визуальный анализ данных о сердечно-сосудистых заболеваниях"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**В задании предлагается с помощью визуального анализа ответить на несколько вопросов по данным о сердечно-сосудистых заболеваниях. Данные использовались в соревновании [ML Boot Camp 5](http://mlbootcamp.ru/round/12/sandbox/) (качать их не надо, они уже есть в репозитории).**\n",
    "\n",
    "**Заполните код в клетках (где написано \"Ваш код здесь\") и ответьте на вопросы в [веб-форме](https://docs.google.com/forms/d/1WBYEAYlgOhqAJyh_e3udmBWpBbkpyFSrFCMlWAoRFTY/edit). Код отправлять никуда не нужно.**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "В соревновании предлагалось определить наличие/отсутствие сердечно-сосудистых заболеваний (ССЗ) по результатам осмотра пациента.\n",
    "\n",
    "**Описание данных.**\n",
    "\n",
    "Датасет сформирован из реальных клинических анализов, и в нём используются признаки, которые можно разбить на 3 группы:\n",
    "\n",
    "Объективные признаки:\n",
    "\n",
    " - Возраст (age)\n",
    " - Рост (height)\n",
    " - Вес (weight)\n",
    " - Пол (gender)\n",
    " \n",
    "\n",
    "Результаты измерения:\n",
    "\n",
    " - Артериальное давление верхнее и нижнее (ap_hi, ap_lo)\n",
    " - Холестерин (cholesterol)\n",
    " - Глюкоза (gluc)\n",
    " \n",
    "\n",
    "Субъективные признаки (со слов пациентов):\n",
    "\n",
    " - Курение (smoke)\n",
    " - Употребление алкоголя (alco)\n",
    " - Физическая активность (active)\n",
    " \n",
    "Целевой признак (который интересно будет прогнозировать):\n",
    " - Наличие сердечно-сосудистых заболеваний по результатам классического врачебного осмотра (cardio)\n",
    "\n",
    "Возраст дан в днях. Значения показателей холестерина и глюкозы представлены одним из трех классов: норма, выше нормы, значительно выше нормы. Значения субъективных признаков — бинарны.\n",
    "\n",
    "Все показатели даны на момент осмотра."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# подгружаем все нужные пакеты\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "# игнорируем warnings\n",
    "import warnings\n",
    "warnings.filterwarnings(\"ignore\")\n",
    "\n",
    "import seaborn as sns\n",
    "\n",
    "import matplotlib\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.ticker\n",
    "%matplotlib inline\n",
    "\n",
    "# настройка внешнего вида графиков в seaborn\n",
    "sns.set_context(\n",
    "    \"notebook\", \n",
    "    font_scale = 1.5,       \n",
    "    rc = { \n",
    "        \"figure.figsize\" : (12, 9), \n",
    "        \"axes.titlesize\" : 18 \n",
    "    }\n",
    ")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "В рамках задания для простоты будем работать только с обучающей выборкой. Чистить данные от выбросов и ошибок в данных НЕ нужно, кроме тех случаев, где об этом явно указано.\n",
    "<br>\n",
    "<br>\n",
    "Все визуализации рекомендуем производить с помощью библиотеки `Seaborn`."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Проведем небольшой EDA"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "train = pd.read_csv('../../data/mlbootcamp5_train.csv', sep=';',\n",
    "                    index_col='id')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Размер датасета:  (70000, 12)\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style>\n",
       "    .dataframe thead tr:only-child th {\n",
       "        text-align: right;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: left;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>age</th>\n",
       "      <th>gender</th>\n",
       "      <th>height</th>\n",
       "      <th>weight</th>\n",
       "      <th>ap_hi</th>\n",
       "      <th>ap_lo</th>\n",
       "      <th>cholesterol</th>\n",
       "      <th>gluc</th>\n",
       "      <th>smoke</th>\n",
       "      <th>alco</th>\n",
       "      <th>active</th>\n",
       "      <th>cardio</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>18393</td>\n",
       "      <td>2</td>\n",
       "      <td>168</td>\n",
       "      <td>62.0</td>\n",
       "      <td>110</td>\n",
       "      <td>80</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>20228</td>\n",
       "      <td>1</td>\n",
       "      <td>156</td>\n",
       "      <td>85.0</td>\n",
       "      <td>140</td>\n",
       "      <td>90</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>18857</td>\n",
       "      <td>1</td>\n",
       "      <td>165</td>\n",
       "      <td>64.0</td>\n",
       "      <td>130</td>\n",
       "      <td>70</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>17623</td>\n",
       "      <td>2</td>\n",
       "      <td>169</td>\n",
       "      <td>82.0</td>\n",
       "      <td>150</td>\n",
       "      <td>100</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>17474</td>\n",
       "      <td>1</td>\n",
       "      <td>156</td>\n",
       "      <td>56.0</td>\n",
       "      <td>100</td>\n",
       "      <td>60</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      age  gender  height  weight  ap_hi  ap_lo  cholesterol  gluc  smoke  \\\n",
       "id                                                                          \n",
       "0   18393       2     168    62.0    110     80            1     1      0   \n",
       "1   20228       1     156    85.0    140     90            3     1      0   \n",
       "2   18857       1     165    64.0    130     70            3     1      0   \n",
       "3   17623       2     169    82.0    150    100            1     1      0   \n",
       "4   17474       1     156    56.0    100     60            1     1      0   \n",
       "\n",
       "    alco  active  cardio  \n",
       "id                        \n",
       "0      0       1       0  \n",
       "1      0       1       1  \n",
       "2      0       0       1  \n",
       "3      0       1       1  \n",
       "4      0       0       0  "
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "print('Размер датасета: ', train.shape)\n",
    "train.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Для начала всегда неплохо бы посмотреть на значения, которые принимают переменные."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Переведем данные в \"Long Format\"-представление и отрисуем с помощью [factorplot](https://seaborn.pydata.org/generated/seaborn.factorplot.html) количество значений, которые принимают категориальные переменные."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA4sAAANHCAYAAACfOcisAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAADl0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uIDIuMS4wLCBo\ndHRwOi8vbWF0cGxvdGxpYi5vcmcvpW3flQAAIABJREFUeJzs3Xu07VdB2PtvyIFglNrURh4lLeW2\nzluUyktRHiItN5cqYql2XC9YHgV18EwRA728rihBLiAKWEsVDEUEqaKIvNQWw7NREeGiwhzgBUxB\nIGiKASKv5P6x1oHNnjkJ++Scs7OTz2eMM/bav/lbc/3W3ueMcb7j91u/edJll10WAAAA7HSd/T4A\nAAAArn7EIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAi0P7fQAHyYUXXmydEQAAuAY5/fQbnLTf\nx3B15cwiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAux\nCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQ\niwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAAL\nsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALA7t9wHA1cVZT3/FMZ/zWWff\n85jPCQAAJ4IziwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsA\nAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EI\nAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAItD+30AAABwbXTW019x\nXOZ91tn3PC7zcu3jzCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAA\nLMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAA\nwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAA\nACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAACLQ/vx\nomOMB1WPrs6o/rQ6e875uu3YmdXTqlG9p3rMnPM1O577tdXPVGdWn6nOrR435/zcjn0eWf276vTq\nzdVD5pzv2TF+u+pZ1a2rD1Y/Pud84XF7wwAAAAfMCT+zOMa4X/UfqqdWt6xeX71ijHGzMcYtqldU\nv9Im5H6jevkY4+t3TPGy6kbVXar7Vw+onrRj/gduv39Udfvqkuq1Y4xTtuOnV79Vva26TfXs6vnb\nSAUAAKATHItjjJPahNz/M+f8hTnne6sfqd5b3aE6qzp/znnOnPPdc84nVG/Zbm+M8a3Vnar7zTnf\nMed8dXV29fDDMdjmjOUz55y/Oud8Z3Xv6mur79mOP6j6eHXW9jWeU71oexwAAAB04s8sjuofVC89\nvGHOeemc81ZzzhdXd67O2/Wc87bb2379wJzzfbvGb1DdanuJ6tftnGPO+YnqrbvmeMOc89Jdc9xx\nG7MAAADXeif6M4tft/36t8cYr6u+oXp39e/nnG+pbtrmM4Q7fajNZxu7gvG2+3x2+/jK5vijyxk/\ntfqa6mNf7psBAAC4pjrRsfi3tl//c/XENqH4oOp1Y4xbtwm2v9n1nE9X198+XsbnnJ8dY1y23efU\n7eY9zbEdb8c+l+u0007t0KGTr2gX+BKnn36D/T4EAOBaxv8/OFZOdCwePvN3zvay08YYD21zaeiD\n29yM5pRdzzml+uT28TI+xrhuddJ2n0t2POfLnmPH95/sClx00aeuaBgWF1548X4fAgBwLeP/H3sj\nro/sRH9m8fDloe88vGHOeVn1ruofVhdUN971nJvseN6Rxg/PfcH28dHM8Yk2N74BAAC41jvRsfi2\nNmfvvunwhu1NZW5R/Vn1pjZLYux01+oN28dvqm4+xjhj1/jF1dvnnB9tszbjF+YYY3xVdbtdc3zb\nrpvZ3LV6866b3gAAAFxrndDLUOecnxpj/FR1zhjjI23OMD6k+l/aLG1xveoPxxhPql7SZtmL27e5\nRLXqv1fnVy8dYzysumH1tDZLZXxmu88zq2eMMd5b/XH1lOovql/bjj+/zfIazx1j/HR1t+3r3P24\nvXEAAIAD5kSfWazNjW2eXv10m1j81urMufHO6l7V91Zvr+5Zfdec8131hUtW71V9pHpjdW71vOrH\nDk8+53xudU6baDy/TYDe/XBMzjk/0iYMb93mrqgPq+4753zd8X3bAAAAB8dJl1122X4fw4Fx4YUX\n+2Fdg5319Fcc8zmfdfY9j/mcAHAinf3Kxx+XeZ9+jycfl3kPkuPxf4/y/4+9Ov30G1hr/Qj248wi\nAAAAV3NiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgIRYBAABYiEUAAAAWYhEAAICF\nWAQAAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgIRYBAABY\niEUAAAAWYhEAAICFWAQAAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACA\nhVgEAABgIRYBAABYiEUAAAAWYhEAAICFWAQAAGAhFgEAAFgc2u8DYG/OfuXjj/mcT7/Hk4/5nAAA\nwMHmzCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EI\nAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCL\nAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAux\nCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQ\niwAAACzEIgAAAAuxCAAAwOLQfh8AAFwVZ7/y8cdl3qff48nHZV4AOCicWQQAAGAhFgEAAFiIRQAA\nABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgIRYBAABYiEUAAAAWYhEAAICFWAQA\nAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgcehEv+AY4xbV\nn1zO0J3nnG8aY5xZPa0a1Xuqx8w5X7Pj+V9b/Ux1ZvWZ6tzqcXPOz+3Y55HVv6tOr95cPWTO+Z4d\n47ernlXduvpg9eNzzhce0zcKAABwgO3HmcVbVh+rbrzrz+9tQ/IV1a+0CbnfqF4+xvj6Hc9/WXWj\n6i7V/asHVE86PDjGeOD2+0dVt68uqV47xjhlO3569VvV26rbVM+unr+NVAAAANqHM4vVN1R/Ouf8\n8O6BMcZZ1flzznO2m54wxrhTdVb1g2OMb63uVN18zvm+6h1jjLOr54wxfmzO+enq0dUz55y/up3z\n3tVfVN9Tvbh6UPXx6qw556XVu8cYt6l+pPrt4/e2AQAADo79OLP4DdW7jjB25+q8XdvO224/PP6B\nbSjuHL9BdavtJapft3OOOecnqrfumuMN21DcOccdxxgn7emdAAAAXEPt15nF648xzq9uVv1x9dg5\n5+9XN23zGcKdPlSdsX18pPG2+3x2+/jK5vijyxk/tfqaNpfIAgAAXKud0FgcY3xFdfPqwurs6tPV\nw6rXby8FPbX6m11P+3R1/e3jZXzO+dkxxmXbfU7dbt7THNvxduxzuU477dQOHTr5inY5kE4//Qb7\nfQjXWH62cHD59wvHl39jx4+fLcfKCY3FOeclY4zTqk9vP1/YGOP+1W2rh7S5Gc0pu552SvXJ7eNl\nfIxx3eqk7T6X7HjOlz3Hju8/2RW46KJPXdHwgXXhhRfv9yFcY/nZwsHl3y8cX/6NHT9+tnsjro/s\nhH9mcc7514dDcfv9pW2W0jijuqDNnVF3uklfvKz0SONt97lg+/ho5vhEmxvfAAAAXOud0FgcY9x2\njPHXY4zb7th2cnWrNsH4pjZLYux01+oN28dvqm4+xjhj1/jF1dvnnB9tszbjF+YYY3xVdbtdc3zb\nrpvZ3LV6866b3gAAAFxrnegb3Lyjen/1n8YYD21zNu8x1d+tnlXdsPrDMcaTqpdU926zVuKDt8//\n79X51UvHGA/b7v+0NktlfGa7zzOrZ4wx3tvm5jlPabN0xq9tx5/fZnmN544xfrq62/Z17n6c3jMA\nAMCBc0LPLM45P1f9i2pWv1n9fnWj6tvmnB+dc76zulf1vdXbq3tW3zXnfNf2+Zdtxz9SvbE6t3pe\n9WM7XuO51TltovH86nrV3Q/H5JzzI23C8NZt7or6sOq+c87XHdc3DwAAcICc8KUz5pwfrO5zBeOv\nql51BeMfbhOMV/QaP1H9xBWMn19985UeLAAAwLXUCb/BDQAAAFd/YhEAAICFWAQAAGAhFgEAAFiI\nRQAAABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgIRYBAABYiEUAAAAWYhEAAICF\nWAQAAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgIRYBAABY\niEUAAAAWYhEAAICFWAQAAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACA\nhVgEAABgIRYBAABYiEUAAAAWYhEAAICFWAQAAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAAYCEWAQAA\nWBza7wMAAK5dzn7l44/5nE+/x5OP+ZwA13bOLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCL\nAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAux\nCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQ\niwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAAL\nsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACw\nEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAA\nC7EIAADA4tB+vfAY41uqN1V3m3Oet912ZvW0alTvqR4z53zNjud8bfUz1ZnVZ6pzq8fNOT+3Y59H\nVv+uOr16c/WQOed7dozfrnpWdevqg9WPzzlfePzeKQAAwMGzL2cWxxhfWf1idfKObbeoXlH9SpuQ\n+43q5WOMr9/x1JdVN6ruUt2/ekD1pB1zPHD7/aOq21eXVK8dY5yyHT+9+q3qbdVtqmdXz99GKgAA\nAFv7dRnqM6v/sWvbWdX5c85z5pzvnnM+oXrLdntjjG+t7lTdb875jjnnq6uzq4cfjsHq0dUz55y/\nOud8Z3Xv6mur79mOP6j6eHXW9jWeU72o+pHj9k4BAAAOoBMei2OM76i+s3rErqE7V+ft2nbedvvh\n8Q/MOd+3a/wG1a22l6h+3c455pyfqN66a443zDkv3TXHHccYJx3N+wEAALgmOqGxOMb4u9Xz25zh\nu2jX8E3bfIZwpw9VZ1zJeNt9brp9fDRznFp9zZW/AwAAgGuHE32Dm/9UvWLO+doxxk13jZ1a/c2u\nbZ+urn+k8TnnZ8cYl233OXW7eU9zbMfbsc8RnXbaqR06dPKV7XbgnH76Dfb7EK6x/Gzh4PLv92Dx\n+zp4/M6OHz9bjpUTFotjjPu1uXHNPz3CLpdUp+zadkr1ySONjzGuW5203eeSHc/5sufY8f0nuxIX\nXfSpK9vlQLrwwov3+xCusfxs4eDy7/dg8fs6ePzOjh8/270R10d2Ii9DvX+by0A/PMb4RDW3218z\nxnhudUF1413PuUlfvGz0SONt97lg+/ho5vhEmxvfAAAA0ImNxe+vblHdavvnf99uf1D1xDZrLt5l\n13PuWr1h+/hN1c3HGGfsGr+4evuc86Nt1mb8whxjjK+qbrdrjm/bdTObu1Zv3nXTGwAAgGu1E3YZ\n6pzzS24sM8Y4/NnBD845PzrGeE71h2OMJ1UvabPsxe2rB2/3++/V+dVLxxgPq25YPa3NUhmf2e7z\nzOoZY4z3Vn9cPaX6i+rXtuPPb7O8xnPHGD9d3W37Onc/1u8XAADgINuvdRYX23UR71V9b/X26p7V\nd80537Udv2w7/pHqjdW51fOqH9sxx3Orc9pE4/nV9aq7H47JOedH2oThras/qh5W3XfO+boT8BYB\nAAAOjBN9N9QvmHP+jzY3p9m57VXVq67gOR9uE4xXNO9PVD9xBePnV9+8p4MFAAC4lrnanFkEAADg\n6kMsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAA\nACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgA\nAMBCLAIAALAQiwAAACzEIgAAwAk2xrj/GON/7PdxXBGxCAAAwEIsAgAAsDi03wcAAABwUI0xfrn6\n/JzzPju2/cfq9Oonq6dVt60uq95YPXDO+cFdc3x79bvVdeecn9tue0F1aM75/dvv/2V1TvUPq3dX\nj51zvvZ4vjdnFgEAAI7eS6rvHGNcr2qMcXL1r6rfqF5V/dfq66szq5tXj9vrC4wxvrH6xeqp1S2r\nn6t+fYxxq2PxBo7EmUUAAICj95rt17tVr66+rfqKNpH4lOon55yXVe8bY7ysusNRvMaPVL8w5/zF\n7fd/Nsa4ffXw6oFX5eCviFgEAAA4SnPOz4wxfq3N2cRXV/+6esWc8y+2l5I+cnsG8BbVN1a/dxQv\n80+qW44xdobhdavfv0oHfyXEIgAAwFXzy9UvjTEe0iYaHzTG+HvVW6s/qn6r+vnqO6s7Xc7zL7uc\nbYd2PX5Gde6ufT59FY/7ColFAACAq+a/VZdWj6yu1yYOf6j66znndxzeaYzx8Oqky3n+Z7Zfb1Bd\ntH188+r/2z6e1c3nnO/dMdeTqr+snn3s3saXEosAAABXwZzz82OMX60eX710zvnZMcZfVn9vjPG/\nVX/W5vLU72lzpnG3P6kuqf6v7Z1U71Xdui/G4k9Vbxpj/H71m20+H/m46p7H8W25GyoAAMAx8JLq\nq9pcklr1X9rcwfS/VH9Y/fM2Zx7/1zHGV+x84pzzr6sfqP6PNuF42+pZO8bPr+6z3edPtvM8YM75\n6uP4fo7dmcUxxk3mnB86VvMBAAAcFHPON7XjEtM55+erB2//7HT4stEXbP8c3v+Xql+6gvlfWr30\n2Bztl+fLPrM4xvj8GOObjjB25zbX0QIAAHANcIVnFscYj6q+cvvtSdUPjDH+xeXsese++KFMAAAA\nDrgruwz1utUTto8vqx5wOft8vvqf1ZOO4XEBAACwj64wFuecT62eWjXGuLS645zzuC78CAAAwP77\nsm9wM+d051QAAIBriT3dDXWMcdfqHm0+x7g7Hi+bc/7QsTowAAAA9s+XHYtjjB+unlH9TXVhdemu\nXS47hscFAADAPtrLmcVHtFn344FzTnc+BQAAuAbby+cQb1g9TygCAABc8+3lzOI7qm+oXn+cjgUA\nAOBq5d6P/qV9+bjdi592n5P2+pwxxsnVk6v7VzeoXls9dM75kaM5hr3E4iOrl4wxLq7eUn1q9w5z\nzg8dzUEAAABwlf1odb/qvtVfVj9bvay609FMtpdYfF113eoFHflmNicfzUEAAABw9MYY16vOqh4x\n5/yd7bbvq943xrjDnPMte51zL7H44NzxFAAA4OroVm0uPT3v8IY55/vHGO+v7tzm6tA9+bJjcc75\ngr1ODgAAwAlx0+3XD+7a/qHqjKOZcC/rLN77yvaZc774aA4CYK/Oevorjsu8zzr7nsdlXgCA4+zU\n6tI552d3bf90df2jmXAvl6G+6AjbL6s+X32uEovAgXb2Kx9/XOZ9+j2efFzmBQDYuqS6zhjj0Jzz\nczu2n1J98mgm3Ess/sPL2fZVba5//ffVvzyaAwAAAOAqu2D79cY7HlfdpPXS1C/LXj6z+IEjDP3J\n9s47z2kTjgAAAJxY76guru7S9qrQMcbNqptVbziaCa9zjA7s/61ue4zmAgAAYA/mnJ9us67iM8YY\ndx9j3Kb65er1c87zj2bOvVyGernGGNetHlh95KrOBQAAwFF7fHXdNmcWr1u9tnro0U62l7uhvqd1\nncWTq69tc+edHznagwAAALg6evHT7nPSfh/Dl2t7Y5tHbf9cZXs5s/jm1li8rPrr6pVzzv96LA4I\nAACA/beXG9zc/zgeBwAAAFcje/rM4hjj+tUDqm+vvrr6WPXG6oVzzkuO+dEBAACwL77su6GOMf5O\n9XvVf6huXX1l9S3Vf6zeOsY47bgcIQAAACfcXs4sPrXNzWy+Zc75+4c3jjG+uXp5dU71kGN7eAAA\nAOyHvayz+N3V43eGYtX2+ydW//JYHhgAAAD7Zy+x+BXVBUcYu6ByGSoAAMA1xF5i8Z3V/3mEsXtX\nf3rVDwcAAICrg718ZvGc6pXbG938cvXh6kZtAvI7O3JIAgAAcMDsZZ3FV48xHlg9pfquHUMfrh40\n5/wvx/rgAAAA2B97WmexOqV6Q/V/V3+num51bvX5Y3xcAAAA++7+55512X687gse8KyTrsrzxxjP\nrQ7NOR90tHPsZZ3Fh7VZY/F/zjnfPed8S/Xn1e9Wzx9jfP/RHgQAAABX3RjjpDHGj1U/dFXn2suZ\nxYdXPzrn/PHDG+ac76seOMb48+rR1Yuu6gEBAACwd2OMm1fPr76hzYm9q2Qvd0M9o3rzEcbeWP2j\nq3owAAAAHLU7tFnW8JbV+67qZHs5s/iB6q7V6y5n7M7VB6/qwQAAAHB05pwvanu15xjjKs+3l1j8\nueppY4zrVr9efbQ6vc2dUc+unnCVjwYAAICrhb0snfFTY4ybVD/cJg4P+1z1nDnn04/1wQEAALA/\n9rR0xpzz7DHGk6tvqb6m+nj1e3POjx2PgwMAAGB/7HWdxeacH69+6zgcCwAAAFcTe7kbKgAAANcS\nez6zCAAAcG3xggc866T9Pob9IhYBAACuYeac335V53AZKgAAAAuxCAAAwEIsAgAAsBCLAAAALMQi\nAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAACLQ/t9AAAAAFdXr77vAy7bj9f9jheee9JenzPGuGH1\ntOrM6iuq36seNef846M5BmcWAQAADrgxxnWqX6++rvru6g7Vx6v/Nsb4mqOZ05lFAACAg+8bq2+t\nbjHnfFfVGOPfVH9VfWf1wr1O6MwiAADAwffn1T2quWPbpduvpx3NhM4sAgAAHHBzzr+sXrVr8yPa\nfHbxt49mTmcWAQAArmHGGPesfqJ65uHLUvdKLAIAAFyDjDHuX72semn16KOdRywCAABcQ4wxHled\nWz23uu+c89IrecoR+cwiAADANcAY49HVk6snzjl//KrOJxYBAAAOuDHGP62eUv1C9fNjjBvtGL54\nzvnJvc7pMlQAAICD7/uqk6t/W/3Frj+PPJoJnVkEAAA4gu944bkn7fcxfDnmnI+tHnss53RmEQAA\ngIVYBAAAYHHCL0MdY9y0+qnqn7eJ1ddWPzzn/NB2/D7VE6u/X72jevic8w92PP8fVT9T3am6qHr2\nnPPpO8ZPbnMHoPtXN9jO/9A550d27HNm9bRqVO+pHjPnfM1xessAAAAHzgk9szjGOKl6VXVaddfq\nLtWNq9/cjt+tzd17frK6TfXO6rfHGKdvx6/XJv4urr65ekz1o2OMH9jxMj9a3a+6b/Vt1U3bLEh5\n+BhuUb2i+pXq1tVvVC8fY3z98XjPAAAAB9GJvgz1htW7qgfNOd8x53xH9czqNmOM06qzq5fMOX9u\nzvmu6oeqv6oOx+D3VDeqHjDn/NM554vbnCE8u74Qk2dVj51z/s6c821t7gp0xzHGHbZznFWdP+c8\nZ8757jnnE6q3bLcDAADQCY7FOeeH55zfN+d8f33hktQfqv6g+nh1x+q8HftfWr2huvN2052rt845\nP7Fj2vOqfzzGuGF1qzaXnu6c4/3V+3fNcV5f6rwd4wAAANd6+7Z0xhjj5dV3t/nc4V2rv119ZfXB\nXbt+qPqm7eObHmG86ozteEfY54wrmeOMAAAAqPZ3ncUnVE+pHl/9Tl8Mwr/Ztd+nq+tvH59aXXg5\n4233ObW6dM752SuZ44pe44hOO+3UDh06+cp2O3BOP/0G+30I11h+thzm78LB43d2sPh9HTx+Z8eP\nny3Hyr7F4pzznVVjjO+rLqi+fzt0yq5dT6k+uX18yRHG2+5zSXWdMcahOefn9jjHJ7sSF130qSvb\n5UC68MKL9/sQrrH8bDnM34WDx+/sYPH7Onj8zo4fP9u9EddHdqLvhnrDbRx+wZzzU9WfVTdpE2w3\n3vW0m/TFy0YvOMJ4230u2D4+mjl2X5oKAABwrXWizyz+g+olY4z3zjnfWjXG+Oo26x3+5zZ3Jb1L\n9Yvbseu0Wf7i57fPf1N1nzHGqdvIrM3nHeec86NjjI+3WVbjLtWLtnPcrLpZmxvlHJ7jLtWP7ziu\nu+4YBwAAqOopj/uVy/bjdR97zr8+aa/PubI17ffqRMfiW6s3Vs8bY/xg9dnqqW0+h/if25xh/M0x\nxh9Vr6t+uPrq6nnb5/96dU714jHG46tbtlk246FVc85PjzF+tnrGGONj1Uern61eP+c8fzvHc6o/\nHGM8qXpJde/q9tWDj+cbBwCiK7TMAAAgAElEQVQAOF52rGl/YZuTYVXPbrOm/W2PZs4TvXTGpdW/\nqt5evbJ6ffXX1V3mnJ+Yc762+sHqUdXbqltUZ845P7Z9/iXV3au/1Wa5jae2WVPxBTte5vHVL7U5\ns/i71Qeq791xDO+s7rXd9vbqntV3bdd1BAAAOIiubE37PTvhN7jZht/9r2D83OrcKxif1T+7gvHP\ntYnNR13BPq9qU90AAAAH3pzzw9UX7g+zc037OedFRzPnfi6dAQAAwDF2OWvaH5UTehkqAAAAx90T\n2tyX5U3V74wx/t7RTCIWAQAArkHmnO+cc/5+m8tST67udzTziEUAAIAD7krWtHdmEQAA4Frq8Jr2\ntzu8Ycea9n96NBO6wQ0AAMDBd2Vr2u+ZWAQAADiCx57zr0/a72P4csw5Lx1j/KvqGW3WtL9+9Vtt\n17Q/mjnFIgAAwDXAla1pv1c+swgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAA\nLMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAA\nwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAA\nACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgA\nAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsA\nAAAsxCIAAACLQ/t9AAAAV9UfPOoRx2Xeb/rJZx+XeQEOAmcWAQAAWIhFAAAAFmIRAACAhVgEAABg\nIRYBAABYiEUAAAAWYhEAAICFWAQAAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAA\nFmIRAACAhVgEAABgIRYBAABYiEUAAAAWYhEAAICFWAQAAGAhFgEAAFiIRQAAABZiEQAAgIVYBAAA\nYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgIRYBAABYiEUAAAAWYhEAAICFWAQAAGAhFgEAAFiIRQAA\nABZiEQAAgIVYBAAAYCEWAQAAWIhFAAAAFmIRAACAhVgEAABgIRYBAABYiEUAAAAWYhEAAICFWAQA\nAGBx6ES/4BjjhtXTqjOrr6h+r3rUnPOPt+P3qZ5Y/f3qHdXD55x/sOP5/6j6mepO1UXVs+ecT98x\nfnL15Or+1Q2q11YPnXN+ZMc+Z26PYVTvqR4z53zNcXrLAAAAB84JPbM4xrhO9evV11XfXd2h+nj1\n38YYXzPGuFv1C9VPVrep3ln99hjj9O3zr9cm/i6uvrl6TPWjY4wf2PEyP1rdr7pv9W3VTauX7TiG\nW1SvqH6lunX1G9XLxxhff3zeNQAAwMFzos8sfmP1rdUt5pzvqhpj/Jvqr6rvrO5TvWTO+XPbsR+q\n/ln1A9VTqu+pblQ9YM75iepPxxj/uDq7+vltTJ5VPWLO+TvbOb6vet8Y4w5zzrdsx8+fc56zPaYn\njDHutN3+g8f9JwAAAHAAnOjPLP55dY9q7th26fbradUdq/MOD8w5L63eUN15u+nO1Vu3oXjYedU/\n3l7eeqs2l57unOP91ft3zXFeX+q8HeMAAADXeif0zOKc8y+rV+3a/Ig2n118a/WV1Qd3jX+o+qbt\n45seYbzqjO14R9jnjCuZ44wAAACo9uEGNzuNMe5Z/UT1zOoD281/s2u3T1fX3z4+tbrwcsbb7nNq\ndemc87NXMscVvcYRnXbaqR06dPKV7XbgnH76Dfb7EK6x/Gw5zN+Fg8fvjPL34Hjysz1+/Gw5VvYt\nFscY969+vvrl6tFtLkOtOmXXrqdUn9w+vuQI4233uaS6zhjj0Jzzc3uc45NdiYsu+tSV7XIgXXjh\nxft9CNdYfrYc5u/CweN3Rvl7cDz52R4/frZ7I66PbF/WWRxjPK46t3pudd/tZxP/qk2w3XjX7jfp\ni5eNXnCE8bb7XLB9fDRz7L40FQAA4FrrhMfiGOPRbdZBfOKc8+Fzzsuqtl/fUt1lx77XabP8xRu2\nm95U3W6MceqOKe+6efr8aJt1GS/eNcfNqpvtmuMufam77hgHAAC41juhl6GOMf5pmyUwfqHNUhc3\n2jF8cZvPLv7mGOOPqtdVP1x9dfW87T6/Xp1TvXiM8fjqlm2WzXho1Zzz02OMn62eMcb4WPXR6mer\n1885z9/O8ZzqD8cYT6peUt27un314OPzrgEAAA6eE31m8fuqk6t/W/3Frj+PnHO+ts1ah4+q3lbd\nojpzzvmxqjnnJdXdq79V/UH11Oqxc84X7HiNx1e/VL2o+t02N8753sODc853Vvfabnt7dc/quw6v\n+wgAAMCJXzrjsdVjr2Sfc9t8nvFI47P6Z1cw/rk2sfmoK9jnVa1LeAAAALC1Lze4AQAA4OpNLAIA\nALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIA\nAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwC\nAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQi\nAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzEIgAAAAuxCAAAwEIs\nAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBCLAIAALAQiwAAACzE\nIgAAAAuxCAAAwEIsAgAAsBCLAAAALMQiAAAAC7EIAADAQiwCAACwEIsAAAAsxCIAAAALsQgAAMBC\nLAIAALAQiwAAACzEIgAAAItD+30A11RnPf0Vx2Xe6/2T4zItAADAl3BmEQAAgIVYBAAAYCEWAQAA\nWIhFAAAAFmIRAACAhVgEAABgIRYBAABYiEUAAAAWYhEAAICFWAQAAGAhFgEAAFiIRQAAABZiEQAA\ngIVYBAAAYCEWAQAAWIhFAAAA/v/27jxut7ne//jrZuPEkUOoDCVDHz8R+omTeZfpqJzSqTiEfqbQ\ntokdB2WOtnIyhYchQx5IOsrQ5nTYKOmYksjHENsUW5MMOxvt3x/f78XVte5xu+99T6/n47Ef977X\n8L2+11rXte71Xt/v+q4Gw6IkSZIkqcGwKEmSJElqMCxKkiRJkhoMi5IkSZKkBsOiJEmSJKnBsChJ\nkiRJajAsSpIkSZIaDIuSJEmSpAbDoiRJkiSpwbAoSZIkSWowLEqSJEmSGgyLkiRJkqQGw6IkSZIk\nqcGwKEmSJElqMCxKkiRJkhoMi5IkSZKkBsOiJEmSJKnBsChJkiRJajAsSpIkSZIaDIuSJEmSpIYJ\nw/niEXEGMCEzd2ubtgUwFQjgQeCgzPxx2/ylgVOBLYDZwHeAQzPz1bZl9gf2A5YCfgbsnZkPts1f\nBzgJWBt4Ejg6My8YqvcpSZIkSaPNsLQsRkRXRBwF7NkxfTXgR8BllCD3Q+CKiHhf22KXA+8ANgF2\nAT4PHNlWxq719wOA9YBZwLSIWKjOXwq4FrgT+ABwMnBODamSJEmSJIYhLEbEisD1wF7AYx2zJwO3\nZuaxmXl/Zn4FuKVOJyI+BGwI7JyZd2fmNcAUYFIrDAJfBk7MzO9n5j3AvwNLA5+q83cDngMm19c4\nBfgucOAQvWVJkiRJGnWGo2VxfeBxYA3gkY55GwHTO6ZNr9Nb82dk5iMd8xcF1qpdVN/bXkZmvgDc\n3lHGTZn5t44yNoiIrrl4P5IkSZI05szzexYz87uUljwionP2cpR7CNs9BSzfx3zqMq/U//dVxl3d\nzF8YeBvw+77egyRJkiSNdcM6wE03Fgb+2jHtZeAfepqfma9ExJy6zMJ18oDKqPNpW6Zbiy++MBMm\nzN/bIqPSUkstOtxVGLPctmrxszD6uM8Efg6Gktt26LhtNVhGWlicBSzUMW0h4MWe5kfEAkBXXWZW\n2zr9LqPt9xfpxZ/+9FJvs0etZ599frirMGa5bdXiZ2H0cZ8J/BwMJbft0HHbDozhumcj7TmLjwPv\n7Ji2DG90K+1pPnWZx+v/56aMFygD30iSJEnSuDfSwuJPKY/EaDcRuKlt/ooRsXzH/OeBX2bmTMqz\nGV8vIyL+EVino4yNOwazmQj8rGPQG0mSJEkat0ZaN9RTgDsi4kjgYspjL9ajPGYD4OfArcClEfFF\n4O3AVMqjMmbXZU4EvhERDwG/Br4G/A74QZ1/DuXxGmdExLeAzerrbDXE702SJEmSRo0RFRYz856I\n+CQlAB4E3A98PDN/U+fPqfNPB26mtCieDRzVVsYZEbE4JTS+ldKSuFUrTGbmMxGxFXAyZVTUGcBO\nmXn9PHqbkqRR4LYD9h30Mj/4zZMHvUxJkobKsIbFzNy0m2lXA1f3ss7TwCf7KPc44Lhe5t8KrNvv\nikqSJEnSODPS7lmUJEmSJI0AhkVJkiRJUoNhUZIkSZLUYFiUJEmSJDUYFiVJkiRJDYZFSZIkSVKD\nYVGSJEmS1GBYlCRJkiQ1GBYlSZIkSQ2GRUmSJElSg2FRkiRJktRgWJQkSZIkNRgWJUmSJEkNhkVJ\nkiRJUoNhUZIkSZLUMGG4KyBJ0nhx1remDUm5u++31ZCUK0ka32xZlCRJkiQ1GBYlSZIkSQ2GRUmS\nJElSg2FRkiRJktRgWJQkSZIkNRgWJUmSJEkNhkVJkiRJUoNhUZIkSZLUYFiUJEmSJDUYFiVJkiRJ\nDYZFSZIkSVKDYVGSJEmS1GBYlCRJkiQ1GBYlSZIkSQ2GRUmSJElSg2FRkiRJktRgWJQkSZIkNRgW\nJUmSJEkNhkVJkiRJUoNhUZIkSZLUMGG4KyBJkiRp8Ey56rAhKfeEjx0zJOVq5LJlUZIkSZLUYFiU\nJEmSJDUYFiVJkiRJDYZFSZIkSVKDYVGSJEmS1GBYlCRJkiQ1GBYlSZIkSQ2GRUmSJElSg2FRkiRJ\nktQwYbgrIEmSJA2Ws741bUjK3X2/rYakXGkkMyxKkiRpnrvtgH2HpuDltx6acqVxyG6okiRJkqQG\nw6IkSZIkqcGwKEmSJElqMCxKkiRJkhoMi5IkSZKkBsOiJEmSJKnBsChJkiRJajAsSpIkSZIaDIuS\nJEmSpAbDoiRJkiSpwbAoSZIkSWowLEqSJEmSGgyLkiRJkqQGw6IkSZIkqcGwKEmSJElqmDDcFZDG\nsilXHTYk5Z7wsWOGpFxJkiSpxZZFSZIkSVKDYVGSJEmS1GBYlCRJkiQ1GBYlSZIkSQ2GRUmSJElS\ng2FRkiRJktRgWJQkSZIkNRgWJUmSJEkNhkVJkiRJUoNhUZIkSZLUYFiUJEmSJDUYFiVJkiRJDYZF\nSZIkSVKDYVGSJEmS1GBYlCRJkiQ1GBYlSZIkSQ2GRUmSJElSg2FRkiRJktRgWJQkSZIkNRgWJUmS\nJEkNhkVJkiRJUoNhUZIkSZLUYFiUJEmSJDUYFiVJkiRJDYZFSZIkSVKDYVGSJEmS1GBYlCRJkiQ1\nGBYlSZIkSQ2GRUmSJElSg2FRkiRJktRgWJQkSZIkNRgWJUmSJEkNhkVJkiRJUoNhUZIkSZLUYFiU\nJEmSJDUYFiVJkiRJDYZFSZIkSVLDhOGuwHCIiPmBY4BdgEWBacA+mfnMcNZLkiRJkkaK8dqyeASw\nM7ATsDGwHHD5cFZIkiRJkkaScRcWI2JBYDJwSGb+d2beCWwHbBAR6w9v7SRJkiRpZBh3YRFYi9L1\ndHprQmY+CjwKbDQsNZIkSZKkEWY8hsXl6s8nO6Y/BSw/j+siSZIkSSNS15w5c4a7DvNUROwInJ+Z\n83dMvx74bWbuNjw1kyRJkqSRYzy2LM4C5ouIzpFgFwJeHIb6SJIkSdKIMx7D4uP15zs7pi9Ds2uq\nJEmSJI1L4zEs3g08D2zSmhARKwArADcNT5UkSZIkaWQZd/csAkTE8cAu9d9M4NvAXzNz0+GrlSRJ\nkiSNHJ337Y0XhwELAN+tP6cB+wxrjSRJkiRpBBmXLYuSJEmSpN6Nx3sWBUTERyNitfr/FSJiTkRs\nONz1UlNETI+Is4e7Hhp8EbFjRMxp+/3RiDhsOOs0UkXEERHx0JssY9C2b0QsHBF7D0ZZfbyOn4lB\nEBGvRsQuw12P8SwizouInwx3PTQ03L9jl2FxHIqIZYGrgKXrpMcpo8P+YtgqJQngg8B/Dncl1C/7\nA18e7kpIkjSUxus9i+NdV/svmfka8PQw1UVSlZnPDncd1G9dfS8iSdLoZlgcxSJiTeA4YH1gYeAR\n4NjMvCAiuoD9gL2BZYEHgEMy8xreeNbkDRFxPnBEXXcjYGXgNGDpzHyxvs6ClDD55cw8OyJWB75Z\nl/8jcDVwUGb+eejf9djU277sZtl1ga8D6wLPUQZqOiQzX42IhYGvAtsB76A8KuaQzPyfefJGxpiI\nWBQ4Hvg3yn65BdgXeBA4BNgZeDfwEvA/wBcy89mI2JQycNYxwJeAuzNzYkR8GDgBWA34JXBNx+s9\nCpydmcfU37eh7M/VgN8D5wLHZOarQ/amh1kv2xygq3bJ3AdYDPgJsHtmPlPXfRcwFfgI8A+UffKl\nzPxtD6/1CeBIIIBHgbOBEzPzb3X+QcCelGPoDOCkzDytdmc8ui4zB5iYmdN7K68+oukR4FDKsfkP\nwJqU72m/6zwWRMTbKaOQbw68CJxI2c7HZOZ5EbE7cCDwLuAh4BuZeX5dd1PKd2s7yufkPcB9wKTM\n/GldZgngVOCjlO/mwd3UYcD7KjNnD/KmGHN627cdy20K3AAsn5lPdDctIhYADqccZ5egHDMPyMxb\n58mbGQPqseogYEXKedx5lM/9V4EPAbcCewFvAS6kfKfOADYFngD2zcxptax+n1/Uc9CzgX8BPpyZ\n90fE8pSeM1sAsyj7+kuZ+dTgv3MNJruhjlIRsQhwHfAUsB7wfspzIs+qB+svUw4IRwNrAJcB/xUR\n7wM+UIv5FDC5o+jvA3OAbdqmbU05kFxWu7DeCPwKWJtyQrca8INBfovjRj/2Zfuy76EcYB+idFnc\nEfgcZV8DXAJ8hvLHeS3KH4JpEbHe0L+TMel7lJP47YF1gBeAa4EDKN+dScAqdf6GlJPLloWAiZRQ\nv29ErEwJhz+l7Jsz6OYktiUitqV8r75HCRVTKKFprHdT7WmbL0A54Vmrzt+Ksm2PA4iItwI/o5xU\nbkk52VkMuDEiFut8kYjYGrgIOAl4H+WYORn4Sp3/8Tptd+C9lEB3SkRsDFxKuWDzBKUL/y19lddm\ne2BjYAdKOOx3nceCiJiPchvEssCHgW0p22LFOn8v4FjKd2l1ynY+KSJ2bitmQUqI2J3yeXgO+E49\nQYXy924NymdkG+CLwPxtdRjwvjIo9q2vfTsXTgZ2pey/NSlhcVpELPXmazv2RcT7gTMp36VVKBc+\nplDOG6D8fVqJ8rdrX0po/AXlu/F/gaSEy5aBnF+cSgmKE2tQXASYTgmJ61OOdwsC19cGCY1gtiyO\nXotQrtidkpkvAUTE14DdKCc2kylXSVstU8fWq3T/CDxZp/0xM5+LiMVbhWbmCxHxA8ofyYvr5B2A\nK+qyU4DfZuaU1joRsR3wRER8KDN/PlRveAzra1+224NydfALtfvwffUq/LvrgEUfB7bMzOvq8pPr\ngfxA4NND/1bGjogIysnmxMycXqftQWlRfBrYuXXFFZgREdMoJ6jtpmbmQ3Xdr1Na9fevLVdZL95M\noXsHA9/LzKn19wdri8nJEXFYZj43KG90BOljm78NmE3Z7q1eD5dSTnignAAtDmyXmX+s8z9NaRHc\nkdJjot0hwLcz89z6+8O1VfOsiDia0stiNjAjM2cAZ0fEb4H7M3NWRLwAvJaZT9fX6qu8llMz8/66\nzt4DrPNYsAnlIsBKrdbTiNgRuKfOPxQ4MjO/X39/OCLeTdlf59dpXZQWjZvr+v8JXAEsGRFLUoLK\nxq2/RzVo3ttWhwHvK/VLX/u23+r++H/Anpn5wzptMiVsLAHYZb9vK1Eu/s/IzMeAxyJiM8pFrlaA\n37MeTx+IiKnAdZl5EUBEfBu4pobzpejn+UVEnAB8Etg0Mx+ok7ennOvsUs9diIjtKT1mPsUb55sa\ngQyLo1RmzoyI04GdImJtylWjterst1Oudv9vxzpHAETEcn0Ufz7lALE48BrwMcoVQiitiWvXE6VO\n/wcwLA5QH/ty/o7F1wDuaB1s6/pXAUTEZ+qkWzrWuZmyDzUwreD3+vcoM/9AaVUkIj4UEcdSurGt\nSvn839xRRntXwtWBu1pdHKveulOtDnR2Q76JctxelbE5IFWP2zwijgCeagXF6k+UXg9Qttf9rdBV\n1/19RNxX53VaG/hgbclqma+WtwKle/eulJB+D6V18+LMnNlD3fsqr7XfOz8TA6nzWPABYGZ7N9vM\n/HVEPEc5IV0W+Ea9uNIyAZjQ0QLxQNv/WxdOFuSN7XZHW/n3RcTzbcvPzb5S33rbtwMVlP3Zfix4\nlRJM1D/TKH8nbo8ykvS1wGWZ+Vi5LsfvOo6nLwIPt/0+q/5ciDe+V32dX2xIuVjzGKW3VMvalO/3\nc/W1Wxam/O3UCGZYHKUiYhlKMHsSuJLS9eMp4HbglTdZ/A3AM5SrPa8Cf6Z0k4Rypf063riHqJ1X\n+uZCH/uyU2/7dlYP0+fvYz11r8dtVu+bOxj4DvBj4GuU1vx3dyzavk/m0BwUpbeubd3tz9bFg7G6\nP/t6X691M621TQf6+Z9N6Vp6UTfznsjM2bUb14aULlNbAwdGxOcz87yBlgcs0009x+N39lV6vgWm\n9X2YROmy1t26LS93M7+L8j1r/b+7slv/H+i+Ut9627f90X5OOlY///NMZs4CNomIdShdQrcC9qkX\n3qD7bfy3bqZB/49Vz1O6fv8X5RaBSXX6bErr/rY0Od7FCOc9i6PX9sCiwEaZeVxmXgksWef9Bfgd\npTvI6yLihtqNdA69qC0fF1LC4meAi9pasu6lXAWakZkP1S52rwHfApYflHc2/vS2LztPeH5Dadl9\n/bsbEXtExB2UQR4ANuhYZ4O2eeq/39Sfr3+PIuKtETGTci/wVzNzUmaek5l3UlqEexsh85eU1oz2\nE6J1elqYss869+WGlD+6DzcXHxN62+Z9PQf2PmDV2lW3te6SlBaK7j7/9wKrtI5j9Vi2BuV+ua6I\n+CywV2belJmHZubalAsDrRb8zuNor+UNUp3Hgl9Ruouu1JpQux8vRmkhfBJYoWM7bgYc2NEq35O7\n68/128pfgdKNuWVu9pX61tu+7dQK729tm7ZK2/8fooTP9mPBfBHxQL31RX2IiM0j4iuZeXtmHp2Z\nGwCnA5+di+L6e35xd+3+PZkSTFvH7Xspg1H9oe07N5NyC07n7RsaYWxZHL0epxxkPxURv6Dc/H1y\nnbcQ5arpERHxAHAbJZD8M+VG8VZ3nPfX7lXdOZ/S3a6LMpJWy6m1jPMi4vj6WqcB/8TfdwtS//W1\nL9udRmnVPSUiTqEE9CMoI2g+HBGXAKdHxBco3UD2oNyovt+Qv4sxJjMfiIgfAt+u3dWepZxMPkcZ\nHXHLiLiGcmV1L8rIcr11DT2Tsu/OrPd0vJ/uW+hbjqF0B7+LcpV2LeAoyr4ec/crQp/b/DZKF8Ge\nXES53+2SiGgNHDSV0lX1km6WPwa4OiJ+DVxOuT/4TOCazHw5IhaidIf8M2VQopUp3exOr+s/Dyxe\nT4Zn9KO8wajzqJeZN0TE7cAFEbEv5aJ1697MOZTteGJEPEYZGXY9ygnl1O7K66b8B9s+Q7tRPjsn\n8/ctJnOzr9SHfuzbdvdQBq86JCIOpwTFA9rKejEiTqOMt/B7ygjU+1Pu8b1haN/JmDEbOLx2A76S\nMoLpRHq//aFbAz2/yMxL673C50QZ7b11rPteRPwH8FfKyKvr8vf3E2sEsmVx9LqM0pp3CuWqztGU\nE8nWKJknU/64TgV+Dfwr8PHMvDcz/1LX+zplaOOGelPyXcB9mXlP2/SnKVd530E5Mb6WctDY3NHi\n5lpf+/J1mfkkpSvJ2pSWqnOBc3hjNNTdKfcpfBe4k3KitYUDD821XSj3zPyQ8nlfkLL9P0e5QHIX\n8N+UVouDgdWiDC/ekJmPU0bxXLWudyjlj2W3MvNaYCfKsPH3Ur7LJ9EcwXis2YXut3l33Q5fl5l/\npXQXfZlyb+f1lKCwUXbzWJ86ONHngH+nHCPPpNwjumedfwFldMwjKRfCzqN0Oz62FnE55ZELvwI+\n2ld5g1HnMWRbymOXbgZ+RDlezQFmZ+YZwH9QBn66jxLsjuaNY1x/7EAJFFdQHq9yJaW3DdD3vteb\n0uO+bV8oM5+n7IN1KPv5KNrCYnUQZXTkcyl/71ajDLDyzBDWf8zIzBspgwTtQdnGV1BGs+/tImVv\nBnp+0Xp02xG1S+zmlEfZXE8ZBXoC5bEaPd0HrhGia86cXnskSpIkDYrazXY9YFrbqIjvoIS5jVsj\nnGr0cd9KY5PdUCVJ0rzyGqU3xYkRcS7lcU5HU3pS+LD10c19K41BdkOVJEnzRGb+ifK8to9Q7lu7\nkTKQyeaZ6QiYo5j7Vhqb7IYqSZIkSWqwZVGSJEmS1GBYlCRJkiQ1GBYlSZIkSQ2GRUnSuBYR0yPi\nJ4O9ztyUK0nSSOKjMyRJ493elAeHS5KkNoZFSdK4lpn3DXcdJEkaiQyLkqQRrz7ke0tg+cz8W9v0\ns4HNgPcAe9R/q1Jus/gNcGxmXl6X3QU4A5gMHEX5G7gucA7wamZuVpdbqs7fGngn8AJwA/ClzJzR\nVq2uiDgK2AtYCLgSOCAzn+7hPcwHHAzsCiwHPAKckJnnvJltI0nSUPGeRUnSaHAhsAywUWtCRCwI\nbAtcBEwCTgMuBz4K7BsqrUQAAAM0SURBVAC8AlwcEcu2lbMgJSx+Htg/Mx9uf5GI6AJ+DHwYOAjY\nAjgC2Bw4vaNOmwCfpATUSZTQem1E9HQh9nTgcOA8ysPLrwLOiohJ/dsEkiTNW7YsSpJGg+nA48B2\nwI112pbA4pQguScwNTO/1lohIh4F7gDWBy6rk7uAozLzmh5eZ1ngeWDfzLyl9doRsTKlRbDdK8CW\nmflUfb1nKEHzY8AV7QtGxHuB3YEpmfnNOvm6iJgfODoizsnMl/reDJIkzTuGRUnSiJeZcyLiImDX\niJiUma9SguMdmXk/sD9ARPwTpRvqysDEuvqCHcX9spfXeQKYGBFdEbECsEotb4NuyvlZKyjWdadF\nxMvAhnSERUpLZRdwZUfL44+A/SjdYaf3vAUkSZr3DIuSpNHiQso9fx+JiJuBbYDDACJiJeBM4CPA\nbOB+4O66XldHOS/09iIRsQNwHLA88EfgLuClbsp5ppvVnwUW62b62+rP7OFll+mtTpIkDQfvWZQk\njQp11NI7gU9T7kt8C+WexPmAq4ElgQ8Ci2TmmsDxA32NiNgQuIDSbXW5zHxbHfjm590svnjHul3A\n0sDMbpZ9rv7cpNax89+1A62rJElDzbAoSRpNLqQExc8C12XmTEpIDOCszLy9dlEF+Jf6cyB/69av\nyx+emU8C1PsKN++mnA0iYtG23/+V0lV1ejfl3lR/LlHreHtm3g68izLy6iIDqKMkSfOE3VAlSaPJ\nxcA3gE8AOwFk5sw6mM2+EfEU8BfK4Df71XUGEsT+t/48NSLOB5YAvgisSXlUxlsyc1ZdZgHKPYjH\nUULf8cD1wE86C83MX0XExcC5EbEipWvr6sCxlPsuHxtAHSVJmidsWZQkjRqZ+QxwHTCLvx9E5hPA\n7yhdSC8F/pnyeIr7aXvcRj/Knw7sU9f5MXAiMIPyiA46yroCuA24BDiB8tiOT2TmnB6K3xk4mRI+\nrwWmUJ7xuE1/6ydJ0rzUNWdOT3/TJEmSJEnjlS2LkiRJkqQGw6IkSZIkqcGwKEmSJElqMCxKkiRJ\nkhoMi5IkSZKkBsOiJEmSJKnBsChJkiRJajAsSpIkSZIaDIuSJEmSpIb/D1miZLu8hncfAAAAAElF\nTkSuQmCC\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x1164ade10>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "train_uniques = pd.melt(frame=train, value_vars=['gender','cholesterol', \n",
    "                                                 'gluc', 'smoke', 'alco', \n",
    "                                                 'active', 'cardio'])\n",
    "train_uniques = pd.DataFrame(train_uniques.groupby(['variable', \n",
    "                                                    'value'])['value'].count()) \\\n",
    "    .sort_index(level=[0, 1]) \\\n",
    "    .rename(columns={'value': 'count'}) \\\n",
    "    .reset_index()\n",
    "    \n",
    "sns.factorplot(x='variable', y='count', hue='value', \n",
    "               data=train_uniques, kind='bar', size=12);"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Видим, что классы целевой переменной `cardio` сбалансированы, отлично!"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Можно также разбить элементы обучающей выборки по значениям целевой переменной: иногда на таких графиках можно сразу увидеть самый значимый признак."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x1164adef0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "train_uniques = pd.melt(frame=train, value_vars=['gender','cholesterol', \n",
    "                                                 'gluc', 'smoke', 'alco', \n",
    "                                                 'active'], \n",
    "                        id_vars=['cardio'])\n",
    "train_uniques = pd.DataFrame(train_uniques.groupby(['variable', 'value', \n",
    "                                                    'cardio'])['value'].count()) \\\n",
    "    .sort_index(level=[0, 1]) \\\n",
    "    .rename(columns={'value': 'count'}) \\\n",
    "    .reset_index()\n",
    "    \n",
    "sns.factorplot(x='variable', y='count', hue='value', \n",
    "               col='cardio', data=train_uniques, kind='bar', size=9);"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Видим, что в зависимости от целевой переменной сильно меняется распределение холестерина и глюкозы. Совпадение?"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Немного статистики по уникальным значениям признаков.**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "age\n",
      "8076\n",
      "----------\n",
      "gender\n",
      "2 [(1, 45530), (2, 24470)]\n",
      "----------\n",
      "height\n",
      "109\n",
      "----------\n",
      "weight\n",
      "287\n",
      "----------\n",
      "ap_hi\n",
      "153\n",
      "----------\n",
      "ap_lo\n",
      "157\n",
      "----------\n",
      "cholesterol\n",
      "3 [(1, 52385), (2, 9549), (3, 8066)]\n",
      "----------\n",
      "gluc\n",
      "3 [(1, 59479), (2, 5190), (3, 5331)]\n",
      "----------\n",
      "smoke\n",
      "2 [(0, 63831), (1, 6169)]\n",
      "----------\n",
      "alco\n",
      "2 [(0, 66236), (1, 3764)]\n",
      "----------\n",
      "active\n",
      "2 [(0, 13739), (1, 56261)]\n",
      "----------\n",
      "cardio\n",
      "2 [(0, 35021), (1, 34979)]\n",
      "----------\n"
     ]
    }
   ],
   "source": [
    "for c in train.columns:\n",
    "    n = train[c].nunique()\n",
    "    print(c)\n",
    "    \n",
    "    if n <= 3:\n",
    "        print(n, sorted(train[c].value_counts().to_dict().items()))\n",
    "    else:\n",
    "        print(n)\n",
    "    print(10 * '-')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*Итого:*\n",
    "- Пять количественных признаков (без id)\n",
    "- Семь категориальных\n",
    "- 70000 объектов"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 1. Визуализируем корреляционную матрицу\n",
    "\n",
    "Для того чтобы лучше понять признаки в датасете, можно посчитать матрицу коэффициентов корреляции между признаками. <br>\n",
    "\n",
    "Постройте [heatmap](http://seaborn.pydata.org/generated/seaborn.heatmap.html) корреляционной матрицы. Матрица формируется средствами `Pandas`, со стандартным значением параметров."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "###  1. Какие два признака больше всего коррелируют (по Пирсону) с признаком `height` ?\n",
    "\n",
    "- Gluc, Cholesterol\n",
    "- Weight, Alco\n",
    "- Smoke, Alco\n",
    "- Weight, Gender"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Ваш код здесь"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 2. Распределение роста для мужчин и женщин\n",
    "\n",
    "Как мы увидели, в процессе исследования уникальных значений пол кодируется значениями 1 и 2, расшифровка изначально не была нам дана в описании данных, но мы догадались, кто есть кто, посчитав средние значения роста (или веса) при разных значениях признака `gender`. Теперь сделаем то же самое, но графически. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Постройте [violinplot](https://seaborn.pydata.org/generated/seaborn.violinplot.html) для роста и пола. Используйте:\n",
    "- hue – для разбивки по полу\n",
    "- scale – для оценки количества каждого из полов \n",
    "\n",
    "Для корректной отрисовки, преобразуйте DataFrame в \"Long Format\"-представление с помощью функции melt в pandas.\n",
    "<br>\n",
    "[еще один пример](https://stackoverflow.com/a/41575149/3338479)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Ваш код здесь"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Постройте на одном графике два отдельных [kdeplot](https://seaborn.pydata.org/generated/seaborn.kdeplot.html) роста, отдельно для мужчин и женщин. На нем разница будет более наглядной, но нельзя будет оценить количество мужчин/женщин."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Ваш код здесь"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 3. Ранговая корреляция"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "В большинстве случаев достаточно воспользоваться линейным коэффициентом корреляции *Пирсона* для выявления закономерностей в данных, но мы пойдём чуть дальше и используем ранговую корреляцию, которая поможет нам выявить пары, в которых меньший ранг из вариационного ряда одного признака всегда предшествует большему другого (или наоборот, в случае отрицательной корреляции)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "##### Постройте корреляционную матрицу, используя коэффициент Спирмена"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3.1 Какие признаки теперь больше всего коррелируют (по Спирмену) друг с другом?\n",
    "\n",
    "- Height, Weight\n",
    "- Age, Weight\n",
    "- Ap_hi, Ap_lo\n",
    "- Cholesterol, Gluc\n",
    "- Cardio, Cholesterol\n",
    "- Smoke, Alco"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Ваш код здесь"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3.2 Почему мы получили такое большое (относительно) значение ранговой корреляции у этих признаков?\n",
    "\n",
    "- Неточности в данных (ошибки при сборе данных)\n",
    "- Связь ошибочна, переменные никак не должны быть связаны друг с другом\n",
    "- Природа данных"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 4. Совместное распределение признаков"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Постройте совместный график распределения [jointplot](http://seaborn.pydata.org/generated/seaborn.jointplot.html) двух наиболее коррелирующих между собой признаков (по Спирмену)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Кажется, наш график получился неинформативным из-за выбросов в значениях. Постройте тот же график, но с логарифмической шкалой (чтобы не получать OverflowError необходимо отфильтровать значения меньше либо равные нулю)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Ваш код здесь\n",
    "\n",
    "# -------------------- #\n",
    "\n",
    "\"\"\"Сетка\"\"\"\n",
    "g.ax_joint.grid(True) \n",
    "\n",
    "\"\"\"Преобразуем логарифмические значения на шкалах в реальные\"\"\"\n",
    "g.ax_joint.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, pos: str(round(int(np.exp(x))))))\n",
    "g.ax_joint.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, pos: str(round(int(np.exp(x))))))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4.1 Сколько чётко выраженных кластеров получилось на  совместном графике выбранных признаков, с логарифмической шкалой? Под кластером в данной задаче понимается плотное скопление точек, в окрестности которого пренебрежительно мало одиночных наблюдений и которое визуально отделимо от других кластеров.\n",
    "\n",
    "- 1\n",
    "- 2\n",
    "- 3\n",
    "- больше трёх"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Ваш код здесь"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 5. Возраст"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Посчитаем, сколько полных лет было респондентам на момент их занесения в базу."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "train['age_years'] = (train['age'] // 365.25).astype(int)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Постройте [Countplot](http://seaborn.pydata.org/generated/seaborn.countplot.html), где на оси абсцисс будет отмечен возраст, на оси ординат – количество. Каждое значение возраста должно иметь два столбца, соответствующих количеству человек каждого класса **cardio** (здоров/болен) данного возраста."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 5. В каком возрасте количество пациентов с ССЗ  впервые становится больше, чем здоровых?\n",
    "- 44\n",
    "- 49\n",
    "- 53\n",
    "- 62"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Ваш код здесь"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}