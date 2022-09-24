# Discord Bot for My Splatoon 3 Server

This is a bot for my Splatoon3 discord server. It can check and send the current and future stage information.

This bot uses the [Spla3 API](https://spla3.yuu26.com/). Thanks to its author!

## Bot Commands：

1. `?now` - List all the current stages. In the order of Turf War, Bankara Challenge, Bankara Open, and Salmon Run.

2. `?next` - List all the next stages. In the order of Turf War, Bankara Challenge, Bankara Open, and Salmon Run.

3. `?turf [n]` - List the current and the next `n-1` Turf War stages on the schedule. The default value for `n` is 2.

4. `?bankara open [n]` -  List the current and the next `n-1` Bankara Open stages on the schedule. The default value for `n` is 2.

5. `?bankara challenge [n]` - List the current and the next `n-1` Bankara Challenge stages on the schedule. The default value for `n` is 2.

6. `?salmonrun [n]` - List the current and the next `n-1` Salmon Run stages on the schedule, as well as the information of weapons. The default value for `n` is 2.

7. `?fest [n]` - List the current and the next `n-1` SplatFest stages on the schedule. The default value for `n` is 2.

## ToDo

- [DONE] The author of the Spla3 API recently added support for the SplatFest informaion. I am going to add that to my bot too.

- Currently, the bot is using the stage images from Discord CDN. Recently, the author of Spla3 API included the urls of stage and weapon images in the API. I am going to use those urls in my bot.

- Support for other language(s).