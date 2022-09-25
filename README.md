# Discord Bot for My Splatoon 3 Server

This is a bot for my Splatoon3 discord server. It can check and send the current and future stage information.

This bot uses the [Spla3 API](https://spla3.yuu26.com/). Thanks to its author!

## Bot Commands

1. `?now [turf|open|challenge|salmonrun|fest]` - List all the current [turf war | bankara-open | bankara-challenge | salmonrun | SplatFest] stages. If no format parameter is given, the info will be displayed in the order of Turf War, Bankara Challenge, Bankara Open, and Salmon Run.

2. `?next [turf|open|challenge|salmonrun|fest]` - List all the next [turf war | bankara-open | bankara-challenge | salmonrun | SplatFest] stages. If no format parameter is given, the info will be displayed in the order of Turf War, Bankara Challenge, Bankara Open, and Salmon Run.

3. `?turf [n]` - List the current and the next `n-1` Turf War stages on the schedule. The default value for `n` is 2.

4. `?bankara open [n]` -  List the current and the next `n-1` Bankara Open stages on the schedule. The default value for `n` is 2.

5. `?bankara challenge [n]` - List the current and the next `n-1` Bankara Challenge stages on the schedule. The default value for `n` is 2.

6. `?salmonrun [n]` - List the current and the next `n-1` Salmon Run stages on the schedule, as well as the information of weapons. The default value for `n` is 2.

7. `?fest [n]` - List the current and the next `n-1` SplatFest stages on the schedule. The default value for `n` is 2.

8. `?getlang` - Show the current language that is used to display the stage and weapon names.

9. `?setlang` - Set the language that is used to display the stage and weapon names. Currently support CN/EN/JP.

10. `?archive [n]` - Show the _n_th entry of a Splatoon 3 databse collected by my server members. If _n_ is not provided, the list of all entries will be shown.

## ToDo

- [DONE] The author of the Spla3 API recently added support for the SplatFest informaion. I am going to add that to my bot too.

- [DONE] Currently, the bot is using the stage images from Discord CDN. Recently, the author of Spla3 API included the urls of stage and weapon images in the API. I am going to use those urls in my bot.

- [DONE] Support for EN & JP languages.

## Screenshot

![Screenshot1](https://zian999.github.io/images/posts/2022/sp3bot-screenshot1.jpg)