QUESTIONS = [
    """Task 1: Logical Puzzle

Cal Alumni: Chris Pine, Brenda Song, Aaron Rodgers, Ashley Judd

Cal Landmarks: Sather Tower, Doe Library, Memorial Glade, Sproul Plaza

Times of Day: Morning, Noon, Afternoon, Evening

Each alumnus visited exactly one of the landmarks at a distinct time of day.

Clues:

1. Aaron Rodgers did not visit in the morning, and he did not visit Memorial Glade.
2. The person who visited Sather Tower did so in the morning.
3. Ashley Judd visited sometime after the person who went to Doe Library but before the person who went to Sproul Plaza. (Order: Doe Library < Ashley Judd < Sproul Plaza)
4. Brenda Song visited earlier in the day than Aaron Rodgers.
5. The person who visited Memorial Glade did not go at noon.
6. Chris Pine visited Sproul Plaza.

Goal: Determine each alumnus’s landmark and the time of day they visited.""",
    """Task 2: Math/Probability

Imagine there are three generative AI research teams:
1. Team A: Produces two text-to-image models (image-focused models).
2. Team B: Produces two text-to-text models (language-focused models).
3. Team C: Produces one text-to-image model (image-focused) and one text-to-text model (language-focused).

You randomly choose one of these teams and evaluate one of their models. The model happens to be a text-to-image model. What is the probability that the other model produced by the same team is also a text-to-image model?""",
    """Task 3: Visual Pattern Recognition

Each training example below shows a pair of inputs and outputs where a specific transformation has been applied to the blocks. Your task is to determine the rule governing the transformation and apply it to the new test input to generate the correct output.

Option 1: To make the output, you have to create a 3x3 matrix and fill it with green color. Next, transfer the purple pattern to the 3x3 matrix. Then, overlay the gray pattern on top of the purple pattern. After that, fill in the green squares with turquoise color and fill in all the purple and gray squares with green color.

Option 2: To make the output, you have to create a 3x3 matrix and fill it with black color. Next, transfer the brown pattern to the 3x3 matrix. Then, overlay the blue pattern on top of the brown pattern. After that, fill in the black squares with red color and fill in all the brown and blue squares with black color.

Option 3: To make the output, you have to create a 3x3 matrix and fill it with white color. Next, transfer the red pattern to the 3x3 matrix. Then, overlay the green pattern on top of the red pattern. After that, fill in the white squares with black color and fill in all the red and green squares with white color.

You can download the text friendly LLM instructions from [here](https://drive.google.com/file/d/10mt1B-Ch9xyuvjDOZlzlo6mG5l9cBlgx/view?usp=sharing).

![Image](images/task_3.png)
""",
    """Task 4: Search

For each of the following five major generative text-based language models—GPT-4, PaLM 2, LLaMA 2, Claude 2, DeepSeek 3—please provide:

1. The organization responsible for its development 
2. The year it was first publicly introduced
3. Whether it is open-source or closed access
4. Its MMLU benchmark score
5. Its GPQA benchmark score""",
    """Task 5: Writing

Draft a professional email responding to the following customer complaint:

*Dear OpenAI Support Team,*

*I’m writing to share my frustration about a service outage with ChatGPT on December 20th, which lasted from 2 PM to 6 PM EST. I was relying on ChatGPT to help prepare for an important presentation, and the downtime completely disrupted my workflow. As a result, I missed a deadline to submit my slides.*

*What made the situation even more stressful was the lack of timely updates. I checked the OpenAI status page and social media, but I couldn’t find any clear communication about what was going on.*

*I’d like to know what caused the outage, what steps OpenAI is taking to ensure this doesn’t happen again, and if you offer any compensation for the disruption.*

*Best regards,*  
*Avery Collins*""",
]
