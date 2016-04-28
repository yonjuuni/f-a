# f-a
Created: Feb 1, 2016

General overview.
Filmadvisor (tentative title) is a web-based application that should make suggestions on the movies or TV shows  to watch based on the free text entry (or a Pick random kind of option). This is not a commercial project, so the main idea is to develop the skills needed to complete it, and it looks quite interesting.

The initial plan is to create the following components:
 1. Web-application: Django + Bootstrap. Display the main page, get user input, show results.
 2. Text recognition module: NLTK. Analyze the text input, search for synonyms, suggest the most relevant movies based on that.
 3. Movie list generator: python. A module that would get the movie list from the database based on the analyzed input and return to the main web application to display.
 4. Database generator: python. A module to keep the initially generated database up-to-date, generate new titles, get related info from IMDB, Netflix, Kinopoisk and keep related title information.
 5. Database: technology TBD.
 6. Session logger.

Thoughts:
 * Input analysis part would be a tough one***
 * Later on I'd need to implement algorithms that would learn to provide better results based on the previous application usage.
 * I need to implement good and yet simple session logger to analyze the user activity.

TODO:
 1. Decide on the database to be used.
 2. Do a market research on the available competitors, see what features or logic can be used in this project.
 3. Have fun! :)


***
It Couldn’t Be Done
BY EDGAR ALBERT GUEST

Somebody said that it couldn’t be done
      But he with a chuckle replied
That “maybe it couldn’t,” but he would be one
      Who wouldn’t say so till he’d tried.
So he buckled right in with the trace of a grin
      On his face. If he worried he hid it.
He started to sing as he tackled the thing
      That couldn’t be done, and he did it!

Somebody scoffed: “Oh, you’ll never do that;
      At least no one ever has done it;”
But he took off his coat and he took off his hat
      And the first thing we knew he’d begun it.
With a lift of his chin and a bit of a grin,
      Without any doubting or quiddit,
He started to sing as he tackled the thing
      That couldn’t be done, and he did it.

There are thousands to tell you it cannot be done,
      There are thousands to prophesy failure,
There are thousands to point out to you one by one,
      The dangers that wait to assail you.
But just buckle in with a bit of a grin,
      Just take off your coat and go to it;
Just start in to sing as you tackle the thing
      That “cannot be done,” and you’ll do it.

