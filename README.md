# 2023년 한국컴퓨터종합학술대회 - KCC 2023 논문 자료
![image](https://github.com/Jinu-uu/test/assets/82719310/ae625296-3f7f-47a3-b0b1-b6605ecc664b)
![image](https://github.com/Jinu-uu/test/assets/82719310/044e1405-e064-4888-91df-be8dae29a4ef)

<h1>위스키 리뷰 데이터 및 캐스크 정보 기반 위스키 향과 맛 분석</h1>
<br/>
<br/>
<h2>논문 동기</h2>
와인과 맥주는 사람들에게 대중적으로 잘 알려져있지만, 위스키는 그렇지 않기 때문에  
사람들이 위스키구매에 어려움을 겪는다. 이를 해결하기 위해서 리뷰데이터를 사용해 위스키를 분석해본다.

<br/>

<h2>데이터 수집과 전처리</h2>
본 논문에서는 파이썬의 selenium을 사용하여 whisky base사이트와 whisky.com 사이트에서 크롤링을 진행하였다.  
이후 리뷰데이터에 한해, 영어가 아닌 발음기호를 영어로 치환시켜주고, 불용어 및 특수문자 처리와 어간추출을  
사용한 뒤 tokenize하여 리뷰 데이터를 전처리 해주었다.  

<br/>

<h2>연구 모델</h2>
연구 모델은 아래와 같다.  

![image](https://github.com/Jinu-uu/test/assets/82719310/ee43e6ad-4f0a-4d00-825e-66776d848551)

먼저 크롤링한 데이터를 mapping해주어 Slice/Schruing mapping을 구성해준 뒤, 이 데이터를 가지고 word2vec모델을
학습시킨다. 이렇게 학습시킨 word2vec과 문서에서 어떤 단어가 가장 중요한지 도출하는 tf-idf, 차원을 축소하는 pca를 사용하여
맛과 바디감의 결과를 도출한다. 향은 맛과 바디감과 같은 방법을 사용하면 결과에 이상이 생겨 문서에서 단어가 가장 많이 나타난 5개를 뽑아주었다.

<br/>

<h2>결과 및 결론</h2>
결과는 아래와 같다.  

![whisky_output](https://github.com/Jinu-uu/test/assets/82719310/65e68316-ac7a-4726-95bd-70a73e98cd79)

이와 같이 위스키의 향과 바디감, 맛에 대해서 분석해보았는데 이로 인해 위스키 구매에 어려움을 겪는
소비자들에게 고민하는 시간을 줄여주는 효과를 볼 수 있을 것으로 보인다.

<br/>
<br/>
<br/>
<h1>실행 방법</h1>

>git clone https://github.com/Jinu-uu/whiskey_analyze.git  
>pip install requirements.txt  
>python main.py

<h1>스택 및 라이브러리</h1>

>window10  
>conda  
>vscode  
>python 3.8    
>라이브러리는 requirements.txt 참조  


<h3>주의사항</h3>

>conda 환경에서 코드를 테스트해본 것이여서 바닐라 파이썬 환경에서 실행시 오류가날 수 있습니다.  
>이때는 conda의 가상환경 설치시 기본으로 깔리는 라이브러리를 추가적으로 설치하면 오류가 나지 않습니다.  
>whiskey base의 프론트 element이 바뀌어서, 오류가 나는 것을 대비해 크롤링한 데이터를 data 폴더에 넣어주었습니다.  
>pip install requirements.txt가 안된다면 pip 대신 !pip을 사용하시길 바랍니다.
