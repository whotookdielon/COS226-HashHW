___Attempt #___: Construction time for tables, construction time for quotes.

___Attempt 1___: 0.436121s, 0.433873s
    For my first attempt, I used a linked list hash table with a simple has funtion that only looked at the first character of each movie title or quote. This did not work very well because many records started with the same letter causing them to be placed in the same bucket. For attempt 1 we ended up with 6,158,798 collisions for titles and 7,919,589 for quotes. Yikes!!! Even though the table had 4,099 buckets, most of them were unused to because our hash function was not set up to spread out the records.

___Attempt 2___: 0.352540s, 0.432641s
    For my second attempt, I kept the linked list method but changed the hash function to FNV-1a. Instead of only using the first character, this function uses every character in the string to calculate a hash value. This required a little bit of research from me, I had ChatGPT explain how FNV-1a hashing worked at a more basic level than I was taught and I was able to look up examples online to incorporate into the code I had already written. The comparison between attempt 1 and 2 was night and day. We only had 10,129 collisions for titles and 5,788 for quotes. I also increased the table size to 20,011 buckets so the records were spread out much more evenly. This also created more unused buckets, but who cares.

___Attempt 3___: 18.707815s, 13.643698s
    For my third attempt, I switched from linked lists to linear probing, instead of keeping the FNV-1a hashing right away, I wanted to see how first-character hashing would perform first. My god I should've stayed curious, attempt 3 had the worst performance out of all 5 attempts. With 111,907,887 collisions for titles and 112,326,553 collisions for quotes, I thought my code was broken because of how long it took to finish the task (~19 seconds for titles and ~14 for quotes.) This test was very helpful still, it showed me how much more a poor hash function can affect linear probing unlike linked lists.

___Attempt 4___: 0.107498s, 0.187404s
    For the fourth attempt, I kept linear probing and finally switched to FNV-1a hashing instead. This made a massive difference and reduced the collisions down to 41,558 for titles and 23,245 for quotes. One thing to note, this still has not beaten attempt 2 yet. The table still had 5,011 unused slots but the better hash function helped prevent long groups of occupied slots from forming. Who cares about unused slots, just like memory leaks...

___Attempt 5___: 0.097570s, 0.146025s
    For my final attempt I added an extra mixing step to the FNV-1a hash function and I increased the table size from 20,011 to 32,771 slots. This reduced collisions even further to 14,611 for titles and 6,585 for quotes. However, it also increased the wasted space to 17,771 unused slots in each table. This showed me that increasing the table size can help reduce collisions but it also uses way more memory.

___Conclusion___:
    Overall, I learned that choosing a good hash function is just as important as choosing how to handle collisions. Attempt 3 was the worse because linear probing combined with poor hash function caused a huge number of collisions and took much longer to construct.
    Attempt 2 has the fewest collisions overall, while 4 provided a good balance between wasted space and performance. Attempt 5 required a much larger table resulting the improved collision counts.
    If I had to choose one implementation, I would use attempt 2 because it had the fewest collisions and it distributed records effectively using linked lists. This assignment helped me undestand how different hash functions, table sizes (shoutout google for this one), and collision-handling methods affect the efficiency of a hash table.
