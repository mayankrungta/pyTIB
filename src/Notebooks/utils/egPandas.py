{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['Untitled1.ipynb',\n",
       " 'pp.ipynb',\n",
       " 'maddur.csv',\n",
       " 'Untitled.ipynb',\n",
       " '.ipynb_checkpoints']"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import os\n",
    "os.listdir()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [],
   "source": [
    "df = pd.read_csv('minhaj.csv')\n",
    "df['label'] = df['name']\n",
    "df['value'] = df['name']\n",
    "df = df.drop(['name'], axis=1)\n",
    "df.to_json('minhaj.json', orient='records')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [],
   "source": [
    "df = pd.read_html('http://mnregaweb4.nic.in/netnrega/writereaddata/citizen_out/panchregpeople_0203034011_eng1819.html')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "'list' object has no attribute 'head'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0mTraceback (most recent call last)",
      "\u001b[0;32m<ipython-input-13-c42a15b2c7cf>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mdf\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mhead\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0m: 'list' object has no attribute 'head'"
     ]
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "'list' object has no attribute 'sort_values'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0mTraceback (most recent call last)",
      "\u001b[0;32m<ipython-input-11-2d74b6302a55>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0msorted\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdf\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msort_values\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mby\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdf\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcolumns\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m11\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mascending\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mFalse\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0m: 'list' object has no attribute 'sort_values'"
     ]
    }
   ],
   "source": [
    "sorted = df.sort_values(by=df.columns[11], ascending=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "'builtin_function_or_method' object has no attribute 'tail'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0mTraceback (most recent call last)",
      "\u001b[0;32m<ipython-input-12-ad2d6342b8f2>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0msorted\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtail\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0m: 'builtin_function_or_method' object has no attribute 'tail'"
     ]
    }
   ],
   "source": [
    "sorted.tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "'builtin_function_or_method' object has no attribute 'loc'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0mTraceback (most recent call last)",
      "\u001b[0;32m<ipython-input-7-9f2beca0c078>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mfiltered\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0msorted\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mloc\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0msorted\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0msorted\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcolumns\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m11\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m!=\u001b[0m \u001b[0;36m0\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0m: 'builtin_function_or_method' object has no attribute 'loc'"
     ]
    }
   ],
   "source": [
    "filtered = sorted.loc[sorted[sorted.columns[11]] != 0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "       S.No Mandal Name   Gram Panchayat          Village  \\\n",
       "55676     9      MADDUR           MADDUR           Maddur   \n",
       "55677    10      MADDUR           MADDUR           Maddur   \n",
       "15929     4      MADDUR        DOREPALLE        Dorepalle   \n",
       "36604    18      MADDUR  JADAVARAO PALLE  Jadavarao Palle   \n",
       "53634     7      MADDUR           MADDUR           Maddur   \n",
       "\n",
       "      Job card number/worker ID Name of the wageseeker Credited Date  \\\n",
       "55676     142000609012011012-02       GOLLA VENKATAMMA    22/05/2017   \n",
       "55677     142000609012011012-02       GOLLA VENKATAMMA    22/05/2017   \n",
       "15929     142000608011010387-07               SATHAYYA    28/04/2017   \n",
       "36604     142000602004010116-03          DANAMBUJJAMMA    05/06/2018   \n",
       "53634     142000609012010759-02             YASHODAMMA    12/05/2017   \n",
       "\n",
       "       Deposit (INR) Debited Date  Withdrawal (INR)  Available Balance (INR)  \\\n",
       "55676            953            0                 0                     1929   \n",
       "55677           1188            0                 0                     3117   \n",
       "15929           1164            0                 0                     4578   \n",
       "36604            214            0                 0                     3446   \n",
       "53634           1119            0                 0                     2319   \n",
       "\n",
       "       Diff. time credit and debit  \n",
       "55676                            1  \n",
       "55677                            1  \n",
       "15929                            1  \n",
       "36604                            1  \n",
       "53634                            1  "
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "filtered.tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [],
   "source": [
    "filtered.to_csv('filtered.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "autoscroll": false,
    "ein.hycell": false,
    "ein.tags": "worksheet-0",
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [],
   "source": []
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
   "version": "3.8.2"
  },
  "name": "pp.ipynb"
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
