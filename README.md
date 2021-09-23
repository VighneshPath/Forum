# Forum

For my final project, I've decided to make a Forum,  where people can ask their doubts related to specific things, which will help people in tough times like Quarantine.

## The Project has the following models: 

 1. **User**
	 - Inherits the AbstractUser default model from Django.
2. **Post**
	- User - Foreign Key to the User model.
	- Title - CharField, used to store the title of a Post
	- Content - TextField, used to store the Contents of a Post, which is then converted to markdown format.
	- TimeStamp - DateTimeField, used to store the Date and time when a user posted a Post.
	- Likes - IntegerField, to keep track of the total likes on a post.
	- Comments - IntegerField, to keep track of the total comments on a post.
3. **Comment**
	- Post - Foreign Key to the Post model.
	- User - Foreign Key to the User model.
	- Content - TextField, used to store the Contents of a Comment, which is then converted to markdown format.
	- TimeStamp - DateTimeField, used to store the Date and time when a user posted a Post.
	- Likes - IntegerField, to keep track of the total likes on a Comment.
4. **Tag**
	- Post - Foreign Key to the Post model.
	- Content - TextField, used to store a single Tag, linked to a post.
5. **PostLike**
	- User - Foreign Key to the User model.
	- Post - Foreign Key to the Post model.
6. **CommentLike**
	- User - Foreign Key to the User model.
	- Comment - Foreign Key to the Comment model.


## Specifications 

 1. **Home:**  
	 - The "home" link in the navigation bar takes the user to a page where they can see all the posts from all users, with the most recent posts first. Logged in users can also create new posts here.
	- If the User is not logged in, the User will be able to view the post, but will not be able to Upvote or Comment on it.
	![](https://media.discordapp.net/attachments/703184836097081406/788732708930453514/e1.PNG?width=1040&height=559)

2. **New Post:**
	- Users who are signed in are able to write a text or picture based post by filling text into a text area using MarkDown format. The Editor used is SimpleMDE, which will help a layman use it to post what they want.
	- Each Post will have
		1.  User
		2.  Time Stamp
		3.  Likes
		4.  Comments
		5.  Tags
		6.  Title
		7.  Content
	![](https://media.discordapp.net/attachments/703184836097081406/788732713754558464/e2.PNG?width=1040&height=559)
3. **New Comment:**
	- Users who are signed in are able to respond to Posts, in a text or picture based comment by filling text into a text area using MarkDown format. It also uses SimpleMDE.
	- Each Comment will have
		1. User
		2. Time Stamp
		3. Likes
		4. Content
	![](https://media.discordapp.net/attachments/703184836097081406/788732707605315595/e5.PNG?width=1040&height=559)
4. **Search by Tags:**
	- The "Search by Tags" link in the navigation bar takes the user to a page where they can entere comma separated tags into a search box.
	- After clicking search, the page searches for all the posts containing all the posts which have the subset of tags which was entered by the User.
	- Additionally, clicking on a tag on a post redirects the user to a Search for the tag they clicked on.
	![](https://media.discordapp.net/attachments/703184836097081406/788732705150861332/e3.PNG?width=1040&height=559)
5. **Search by Title:**
	- The Search bar in the navigation bar is used to search for Posts matching the title entered in the search bar.
	- All Posts containing the Search term as a substring are then displayed to the User.
	![](https://media.discordapp.net/attachments/703184836097081406/788732707508322314/e4.PNG?width=1040&height=559)
6. **Like and  Unlike Posts and Comments:**
	- The User can like and unlike posts or comments.
	- ReactJS is used to make this process appear smooth.
7. **Edit Post:**
	- A user who posted a post, has the option to Edit it.
	- Clicking on the Edit Button, takes the User to a Page with the Title, Tags and Content of the Post pre-entered in input and textarea fields.
	- The User can then modify what he/she wants.
8. **Post:**
	- Clicking on a "Comment" on a Post, takes the User to the Posts page, if the user is authenticated, Where the User can Comment or see other Comments on that Post.
	![](https://cdn.discordapp.com/attachments/703184836097081406/788966826779475998/Capture.PNG)

## Files
1. **final_project** - Contents of the Django Application are stored.
	1. **views.py** - 
		- Contains the following functions - 
			- **index** - Used for handlings requests to default route. It is the "Home" link in the navigation bar.
			- **login_view** - Used to handle login requests from the login page. Redirects user to the "Home" link once they have been authenticated.
			- **logout_view** - Used to handle logout requests. Redirects user to the "Home" link once they have been logged-out.
			- **register** - Registers a new User  using the attributes of the AbstractUser Class.
			- **liked_post** - Used as an API call to dynamically update the number of likes of a Post, when a User clicks the like button on a Post.
			- **liked_comment** -   Used as an API call to dynamically update the number of likes of a Comment, when a User clicks the like button on a Comment.
			- **post** - Takes User to a particular Posts page, where Details of a post along with its comments is displayed.
			- **search_by_tag** - Takes the request along with comma separated tags. Posts containing those tags are then searched and returned.
			- **search_tag** - When a Tag on a post is clicked, creates a session variable, then the search_by_tag function is called, which uses the session variable to search for Posts in the same manner.
			- **search_by_title** - Takes the request along with a string containing the search term. Posts with title containing the search term are then searched and returned.
			- **edit_post** - Takes a request and a Post id, if the user is authenticated and the Post is made by the user, then the changes in the post in taken from request.POST and used to alter the post with the Post id.
	2. **templates/final_project**
		- **edit_post.html** - Used to render input and textarea field, where a user can edit his/her post.
		- **index.html** - Used to render all the Posts in the database. Each Post has a React Component which is used to keep track of "like" status from the current user as well as to perform fetch requests to update the count of the likes on a post.
		- **layout.html** - Used to render the navigation bar and theme of the website. It is inherited in the rest of the files.
		- **login.html** - Used to render the login page, where the users can login.
		- **post.html** - Used to render a particular Posts page. Each Post and Comment has a React Component which is used to keep track of "like" status from the current user as well as to perform fetch requests to update the count of the likes on a post or comment.
		- **register.html** - Used to render the login page, where the users can register.
		- **search_by_tags.html** - Used to render a page where all the posts containing searched tags are displayed.
		- **search_by_title.html** - Used to render a page where all the posts containing searched title are displayed.

## Distinctiveness and Complexity
1. The Project Uses various concepts like Tags and Comments in which a User can interact with different Posts.
2. The ability to comment gives the user the freedom to answer questions and react to posts.
3. Tags can be used to classify Posts. Thus a User can find Posts related to his/her preference, and help answer/react to them.

## Link to YouTube video - 
[![Watch the video](https://media.discordapp.net/attachments/703184836097081406/788732713754558464/e2.PNG?width=1040&height=559)](https://youtu.be/AdytgRQ5zqU)

## Time Stamps - 
00:07 Register

00:21 Create Post

00:49 Edit Post

01:10 Like Post

01:15 Comment

01:25 Like Comment

01:36 Search By Tags

01:50 Comment by Image

02:30 Search By Title

02:42 Log Out
