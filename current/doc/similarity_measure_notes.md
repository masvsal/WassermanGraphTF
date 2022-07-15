- overlap coefficient is highly biased toward sparesely connected nodes (SCN). SCN will have low neighborhood size, causing them to tend toward higher similarity scores. Take for example a node with 1 relationship which connects to a neighbor which has 100. By the definition of overlap coefficient, the size of the intersecting neighborhood set is 1 and the minimum neighborhood size is 1, so the two nodes are 100% similar.

good example of this dynamic:

![Screen Shot 2022-07-14 at 6 26 19 PM](https://user-images.githubusercontent.com/95512439/179128239-2a70a4ba-4e42-4d41-bd65-8603f3498003.png)
![image](https://user-images.githubusercontent.com/95512439/179128380-029473c3-4bc3-4af6-87ca-3e59607de537.png)
