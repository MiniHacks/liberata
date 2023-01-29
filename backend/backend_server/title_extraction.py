import os
import openai
import tiktoken
import asyncio
from pydantic import BaseModel

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    import sys
    print("Could not find OPENAI_API_KEY -- check your env vars, and if you're having trouble, ask Ritik for help", file=sys.stderr)
    raise

class BookIdeaRow(BaseModel):
    og_text: str
    title: str
    author: str | None

    class Config:
        frozen = True

TOKEN_LIMIT = 2000
enc = tiktoken.get_encoding("gpt2")
async def extract_book_titles(text_block: str) -> list[BookIdeaRow]:
    tokens = enc.encode(text_block)
    print(type(tokens))
    i = 0
    
    tasks = []
    while i < len(tokens):
        tasks.append(asyncio.create_task(openai.Completion.acreate(
            model = "text-davinci-003",
            prompt = "Identify the book titles that are in the following block of text. "
                    "Do not provide book titles that are not mentioned in the text. "
                    "If you are not sure about who the author is,  write 'Unknown' in the table. "
                    "Provide the original snippet of text that made you recognize a book title. "
                    "Record every book you recognize, even if the title is not explicitly mentioned. "
                    # "Try to make the table as long as possible. "
                    "Use the following format:\n"
                    '"<original text 1>" || <book 1> || <author 1>\n'
                    '"<original text 2>" || <book 2> || <author 2>\n'
                    '...\n'
                    '\n'
                    "Text block:\n"
                    f"{enc.decode(tokens[i:i+TOKEN_LIMIT])}\n\n"
                    "Text || Title || Author\n"
                    "----------------------------\n",
            temperature = 0.76,
            max_tokens = 900
        )))

        i += TOKEN_LIMIT

    ret: list[BookIdeaRow] = []

    for task in tasks:
        result = await task
        out: str = result["choices"][0]["text"]
        print(f"\n\n\nllm out:\n{out}")
        books = [
            tuple(cell.strip() for cell in row.split("||"))
            for row in out.split("\n")
        ]
        for triple in books:
            if len(triple) == 3:
                og_text, title, author = triple
                if title != 'Unknown':
 distinction in theater.[14][12] After graduation, he started the Utah Valley Repertory Theatre Company, which for two summers produced plays at "the Castle", a Depression-era outdoor amphitheater.[15] After going into debt with the community theatre's expenses,[16] Card took part-time employment as a proofreader at BYU Press, moving on to full-time employment as a copy editor.[17] In 1981, Card completed his master's degree in English at the University of Utah where he studied with François Camoin and Norman Council. He began a doctoral program at the University of Notre Dame but dropped out to pursue his more lucrative writing projects.[18][9]

Personal life[edit]
In 1977, Card married Kristine Allen,[19] who is the daughter of Mormon historian James B. Allen.[9] The two met when Kristine was in the chorus of a roadshow Card directed before his mission. They courted after Card's mission, and Card was impressed with her intellectual rigor.[20]: 1:30 

After their marriage they had five children; their son Charles had cerebral palsy and died aged 17; their daughter Erin died the day she was born.[21][22] Card's short story, Lost Boys, is highly autobiographical, but contains the death of a fictional child. One of Card's workshop readers, Karen Fowler, said that Card had pretended to experience the grief of a parent who has lost a child. In response, Card realized that the story expressed his grief and difficulty in accepting Charles's disability.[1]: 119  Card stated that he rarely discusses Charles and Erin because his grief has not faded over time.[20]: 1:35:15 

Card and his wife live in Greensboro, North Carolina; their daughter Emily, along with two other writers, adapted Card's short stories Clap Hands and Sing, Lifeloop, and A Sepulchre of Songs for the stage in Posing as People.[23] Card suffered a mild stroke on January 1, 2011, and made a full recovery.[21][24]

Works[edit]
Main article: Orson Scott Card bibliography
Early work[edit]
In 1976 Card became an assistant editor at the LDS Church's magazine Ensign and moved to Salt Lake City.[25] While working at Ensign, Card published his first piece of fiction,[26] a short story called Gert Fram, which appeared in the July 1977 issue of Ensign under the pseudonym Byron Walley.[27]: 157  Between 1978 and 1988, Card wrote over 300 half-hour audioplays on LDS Church history, the New Testament, and other subjects for Living Scriptures in Ogden, Utah.[28]

Card started writing science fiction short stories because he felt he could sell short stories in that genre more easily than others.[29] His first short story The Tinker was initially rejected by Analog Science Fiction and Fact. Ben Bova, the editor of Analog, rejected a rewrite of the story but asked Card to submit a science fiction piece.[30] In response, Card wrote the short story ender's Game, which Ben Bova published in the August 1977 issue of Analog.[31] Card left The Ensign in 1977 and began his career as a freelance writer in 1978.[32][1]: 122  ben bova continued to work with card to publish his stories and his wife barbara bova became card's literary agent, a development that drew criticism of a possible conflict of interest.[33] Nine of Card's science fiction stories, including Malpractice, Kingsmeat, and Happy Head, were published in 1978.[34]

Card modeled Mikal's Songbird on ender's Game, both of which include a child with special talents who goes through emotional turmoil when adults seek to exploit his ability.[35] Mikal's Songbird was a Nebula Award finalist in 1978 and a Hugo finalist in 1979—both in the "novelette" category.[36][37] Card won the John W. Campbell Award for best new writer in 1978 for his stories published that year; the award helped Card's stories sell internationally.[38] Unaccompanied Sonata was published in 1979 issue of Omni and was nominated for both the Hugo and Nebula awards for a short story.[39][40] Eighteen Card stories were published in 1979.[41]

Card's first published book, "Listen, Mom and Dad...": Young Adults Look Back on Their Upbringing (1977) is about child-rearing. He received advances for the manuscripts of Hot Sleep and A Planet Called Treason, which were published in 1979.[42][43] Card later called his first two novels "amateurish" and rewrote both of them later.[44] A publisher offered to buy a novelization of Mikal's Songbird, which Card accepted; the finished novel is titled Songmaster (1980).[45] Card edited fantasy anthologies Dragons of Light (1980) and Dragons of Darkness (1981), and collected his own short stories in Unaccompanied Sonata and Other Stories (1981). In the early 1980s, Card focused on writing longer works, only publishing ten short stories between 1980 and 1985. He published a few non-fiction works that were aimed at an LDS audience; these include a satirical dictionary called Saintspeak, which resulted in him being temporarily banned from publishing in church magazines.[46] Card wrote the fantasy-epic Hart's Hope (1983) and a historical novel, A Woman of Destiny (1984), which was later republished as Saints and won the 1985 award from the Association for Mormon Letters for best novel.[41] He rewrote the narrative of Hot Sleep and published it as The Worthing Chronicle (1983), which replaced Hot Sleep and the short-story collection set in the same universe, Capitol (1979).[18] The recession of the early 1980s made it difficult to get contracts for new books so Card returned to full-time employment as the book editor of Compute! magazine that was based in Greensboro, North Carolina, for nine months in 1983.[47] In October of that year, Tom Doherty offered a contract for Card's proposed Alvin Maker series, which allowed him to return to creative writing full-time.[48]

Late 1980s: ender's Game and short stories[edit]
See also: ender's Game (novel series)
Card's 1977 novella ender's Game is about a young boy who undergoes military training for space war. Card expanded the story into a novel with the same title and told the backstory of the adult Ender in speaker for the Dead. In contrast to the fast-paced ender's Game, speaker for the Dead is about honesty and maturity.[49] ender's Game and speaker for the Dead were both awarded the Hugo Award and the Nebula Award, making Card the first author to win both of science fiction's top prizes in consecutive years.[50][51] According to Card, some members of the Science Fiction and Fantasy Writers of America (SFWA) resented his receiving of the Nebula award while editing the Nebula Awards Report. Subsequently, Card left the SFWA.[52] card attended many science fiction conventions in the late 1980s. he held several "secular humanist revival meetings" at the conventions, satirizing evAngelical revival meetings.[53][54][46]

Card continued to write short stories and columns and published two short story collections: Cardography (1987) and The Folk of the Fringe (1989). The novella Eye for Eye was republished with another novella by Tor and won the Hugo Award for best novella in 1988.[55][56] Between 1987 and 1989, Card edited and published a short science fiction review magazine called Short Form.[46][57] He also wrote characters & viewpoint (1988) and how to Write Science Fiction and Fantasy (1990).[58] Card also offered advice about writing in an interview in Leading Edge #23 in 1991.[59] He wrote the script for an updated Hill Cumorah Pageant in 1988.[60]

Inspired by Spenser's Faerie Queene, Card composed the long poem Prentice Alvin and the No-Good Plow, which uses colloquial language and diction common to joseph smith's time. the poem, along with the novelette "Hatrack River,"[61] became the basis for seventh Son (1987), the first book in The Tales of Alvin Maker series, a fantasy retelling of the Joseph Smith story. in the alternate history novel, alvin maker, the seventh Son of a seventh son, is born with unusual magical abilities that make him a "maker." alvin has many similarities to joseph smith. following seventh Son, he wrote red Prophet, and Prentice Alvin, which focus on settlers' interactions with indigenous peoples and slaves, respectively.[58][62][63] The series has sustainable environmental ethics as a main theme, addressing ways humans affect the environment in the Americas.[61] alvin maker's life has many parallels with joseph smith's. seventh Son won the 1988 Mythopoeic Fantasy award, and the two following books were nominees.[64] The awards are given to books that exemplify "the spirit of The Inklings".[65] Critics praised seventh Son for creating an American mythology from American experience and belief.[66] According to literary critic Eugene England, the series brings up questions about what, exactly, the mission of a religious prophet is. The series also questions the difference between a prophet and magician, religion and magic.[67]

In the 1980s, Card also wrote Wyrms (1987), a novel about colonizing a planet, and revised A Planet Called Treason, which was published as Treason.[58] He also novelized James Cameron's film The Abyss.[68][69]

Works from the 1990s[edit]
Card wrote prolifically in the 1990s, including many books and the short story omnibus Maps in a Mirror (1990). card continued the ender's Game series with Xenocide (1991) and Children of the Mind (1996), which focus on Jane, an artificial intelligence that develops self-awareness. These books were considered inferior to their predecessors and were, according to science fiction critic Gary Westfahl, "overly prolonged".[70][51]

While Children of the Mind concluded the initial ender's Game series, card started another series of books and continued writing in The Tales of Alvin Maker series. the Homecoming Saga is a science-fiction adaptation of The Book of Mormon.[71] The series' volumes; The Memory of Earth, The Call of Earth, The Ships of Earth, Earthfall, and Earthborn were published between 1992 and 1995.[72] alvin Journeyman (1995), the fourth book in The Tales of Alvin Maker series, won a locus award and Heartfire (1998) was a nominee for the same award.[73][74]

Card wrote several stand-alone novels in the 1990s. Pastwatch: The Redemption of Christopher Columbus (1996) examines time travel and Christopher Columbus.[75] Card collaborated with Star Wars artist Doug Chiang on Robota[76] and with Kathryn H. Kidd on Lovelock.[77] Lost Boys (1992) is a horror story with a semi-autobiographical background.[78] treaSure box (1996) and Homebody (1998) represent Card's foray in horror. Enchantment (1999) is a fantasy novel based on the Russian version of Sleeping Beauty.[79][80] It deals with a couple who learn to love each other after they marry. Card stated: "I put all my love for my wife into [Enchantment]."[20]: 1:06 

Shadow series and later writings[edit]
in 1999, card started a spin-off "shadow" series in the ender's Game universe that is told from the point of view of other characters. these novels are Ender's Shadow, shadow of the Hegemon, Shadow Puppets, Shadow of the Giant and Shadows in Flight, the latter serving as a bridge to the final book The Last Shadow, which is also a sequel to Children of the Mind.[81][82] Westfahl praised the Shadow series, stating they were "executed with panache and skill".[51] Card wrote other spin-offs: a series of shorter stories, First Meetings in the Enderverse, and novels a War of Gifts,[83] and ender in Exile.[84][85] Aaron Johnston and Card conceptualized the stories that make up the prequel to ender's Game, realizing many of them would work best in novel format but first publishing the comics through Marvel. The Burning Earth and Silent Strike comic series were published in 2011 and 2012.[86][87][88] Card and Johnston co-wrote the novels in the series between 2012 and 2019; these are earth Unaware, earth Afire, earth Awakens, the Swarm, and the Hive. children of the Fleet is the first novel in a new sequel series, called Fleet School.[89][90][88]

While Card was writing books in the Shadow series, he also wrote a series of books focused on women in the Bible, novellas, and other novels. Card's The Women of Genesis series includes sarah (2000), rebekah (2002), and rachel and Leah (2004).[91] Card wrote three novellas in the 2000s; space Boy (2007) is a children's story, hamlet's Father (2008) is a retelling of Shakespeare's Hamlet, and stonefather (2008) is the first story set in the mithermages universe.[92][93][94] the Crystal City (2003), is the sixth book in The Alvin Maker series.[61]

Card wrote two young-adult fantasy trilogies in the 2010s. mithermages is about a teenager growing up on a magical estate in rural Virginia; it includes The Lost Gate (2011), The Gate Thief (2013), and Gatefather (2015).[89][95] The pathfinder trilogy consists of pathfinder (2010), Ruins (2012), and Visitors (2014), and follows a young man who can change the past.[96][89] Card has also written several urban fantasies, including magic Street (2005) and lost and Found (2019), both of which are about teenagers with special powers.[97][98]

Card wrote the Christmas novel zanna's Gift (2004), which was originally published under a pseudonym.[99] a Town Divided by Christmas and a "Hallmark Christmas movie in prose" were published in 2018.[100] invasive Procedures (2007), a medical thriller co-written with Aaron Johnston, is based on a screenplay Johnston wrote, which is based on Card's novel Malpractice.[101]

Video games, comic books and television[edit]
In the 1990s, Card contributed dialogue to the point-and-click adventure video games The Secret of Monkey Island, The Dig, and NeoHunter, an early first-person shooter.[102][103] His collaboration on videogame scripts continued in the 2000s, when he worked with Cameron Dayton on Advent Rising[104][105] and outlined the story for Shadow Complex, a prequel to the events in his novels Empire and Hidden Empire. The novels and game are about a near-future civil war in the United States that occurs after civilians resist a left-wing coup in the White House.[51][106][107]

Card has written scripts for the two-volume comic-book series Ultimate Iron Man.[108] He collaborated with his daughters Emily and Zina on the graphic novel Laddertop,[109][110] and with Aaron Johnston to write a series of six Dragon Age comics.[111] In 2017, Card wrote, produced, and co-created a television series called Extinct for BYU TV that ran for one season before it was canceled.[112][113]

Adaptations[edit]
See also: ender's Game (comics)
Many of Card's works have been adapted into comic books. Dabel Brothers Productions published comic-book adaptations of red Prophet and Wyrms in 2006.[114] Aaron Johnston wrote comic-book versions of ender in Exile and speaker for the Dead.[115] Marvel published two ender's Game miniseries, which were collected in the graphic novel version of ender's Game; Christ Yost wrote the script and Pasqual Ferry was the artist.[116][117] Two sets of comic miniseries were adapted by Mike Carey for Ender's Shadow and the comics collected in Ender's Shadow Ultimate Collection.[118] A series of one-shots, some of which are based on Card's Enderverse short stories, were collected in ender's Game: War of Gifts.[119][120][121]

Since ender's Game was published in 1985, Card was reluctant to license film rights and artistic control for the novel. He had two opportunities to sell the rights of ender's Game to Hollywood studios, but refused when creative differences became an issue.[122][123] Card announced in February 2009 that he had completed a script for Odd Lot Entertainment, and that they had begun assembling a production team.[124] On April 28, 2011, it was announced that Summit Entertainment had picked up the film's distribution and Digital Domain joined Odd Lot Entertainment in a co-production role.[125] Card wrote many versions of the script for the movie,[126] but ultimately director Gavin Hood wrote the screenplay. Card was a co-producer of the film.[127][128][129] On Rotten Tomatoes, the critical consensus states: "If it isn't quite as thought-provoking as the book, ender's Game still manages to offer a commendable number of well-acted, solidly written sci-fi thrills."[130]

Newspaper columns[edit]
Since 2001, Card's commentary includes the political columns "War Watch",[131] "World Watch",[132] and "Uncle Orson Reviews Everything", which were published in the Greensboro Rhinoceros Times until 2019.[133][134] "uncle orson reviews everything" features personal reviews of films and commentary on other topics. the column also appears on card's website, which is titled "Hatrack River".[135] From 2008 to 2015, Card wrote a column of Latter-day Saint devotional and cultural commentary for the Nauvoo Times, which was published through Hatrack River.[136]

Influences and style[edit]
Influences[edit]
During his childhood, Card read widely. He read children's classics and popular novels.[137] His favorite book was Mark Twain's The Prince and the Pauper and he read his family's World Book Encyclopedia in its entirety. He read science fiction stories in anthologies and science fiction novels.[5][138][33] He especially credits Tunesmith by Lloyd Biggle Jr. as having a large effect on his life.[5] Card often refers to works by Robert A. Heinlein and J. R. R. Tolkien as sources of inspiration.[139] Card credits C. S. Lewis's apologetic fiction in the Chronicles of Narnia and The Screwtape Letters[140]: 1:17:50  as influences that shaped his life and career.[141] In 2014, Card stated that Isaac Asimov and Ray Bradbury were conscious influences on his writing, along with Early Modern English from the King James Version of the Bible and the works of William Shakespeare.[142] As a college student, Card read classic literature, science fiction, and fantasy.[139] Spenser's poetry inspired the original Prentice Alvin and the No-Good Plow.[62][143] Influences from Portuguese and Brazilian Catholicism, which Card learned about during his LDS mission to Brazil, are evident in his Shadow and Speaker novels.[12] Card stated his writing improved after teaching writing workshops with Jay Wentworth and from Algis Budrys's workshops at Writers of the Future.[9]

card's membership of the lds church has been an important influence on his writing, though he initially tried to keep his religious beliefs separate from his fiction.[144][145] Susanne Reid, a science fiction scholar,[146] stated Card's religious background is evident in his frequent messiah protagonists and the "moral seriousness" in his works.[147][148] Card's science-fiction books do not reference the LDS religion directly but "offer careful readers insights that are compelling and moving in their religious intensity".[149] Non-LDS readers of A Planet Called Treason did not remark on religious themes, however, LDS reviewer Sandy Straubhaar disliked the novel's explicit violence and sex, and stated LDS connections were "gratuitous".[149] Dick Butler criticized A Planet Called Treason for its lack of Gospel themes and ideas, and two other LDS reviewers defended Card.[150] According to Michael Collings, a critic who acknowledges his "unabashed appreciation" of Card,[151] knowledge of Mormon theology is vital to completely understanding Card's works, stating the life stages of the "piggies" in speaker for the Dead correspond to phases of life in the LDS's plan of salvation.[152]In an article in Sunstone, christopher c. smith also noticed this parallel, noting that the "piggies" procreate "more or less eternally" in the last stage of their development.[153] ender's Game and speaker for the Dead deal with religious themes common in lds theology but without many Surface references to the religion.[154] the alvin maker series does not try to explain mormon history but uses it to examine his characters' relationships with god.[155] Card stated that his church membership influences his communitarian values, specifically, making personal sacrifices for the good of a community. Individuals making sacrifices for their community is a theme in his work.[156]

Card's Homecoming Saga is a dramatization of Book of Mormon. Eugene England called the first five novels "good literature". Card received criticism from members of the LDS church for "plagiarizing" the Book of Mormon and using it irreverently. He defended his choices and said speculative fiction is the genre best suited to exploring theological and moral issues.[157] Also in the Homecoming Saga, Card imagines backstories and explanations for "anomalies" in the Book of Mormon, making the fictional work function as a work of Mormon apologetics.[158] While women are not prominent in the Book of Mormon, Card makes them prominent in his retelling.[159] One non-LDS critic described the saga as "readable" but lacking in new ideas.[160] Unaware of its relation to the Book of Mormon, another critic said it is similar to the Bible.[161]

Style[edit]
because card began his writing career in screenplays, his early work is considered accessible and fast-paced with good characters, but also stylistically unremarkable. according to biographer richard bleiler, a number of critics described his tone as emotionless or conversely, as nonjudgmental, leaving readers to come to their own conclusions about how to feel about a story.[162] Though Card was initially classified as a hard science fiction writer for publishing in Analog,[163] his science fiction focuses more on his characters than on the details of future technology.[162] one critic said card is poor at characterization, stating the characters peter and valentine in ender's Game are "totally unbelievable".[164] While noticing that some of Card's early stories were formulaic, Westfahl praised many of Card's early stories as showing "conspicuous originality".[165] the graphic violence in his early fiction was controversial; frequent appearances of naked men and boys raised "questions about homoerotic imagery" according to westfahl.[166] Collings stated that the early stories are "essential steps in the development of Card's fiction".[167] Card uses a technique common in pulp fiction when he refers to characters by a quirk of their appearance or personality.[51] Card's fantasy stories also use tropes that are common to fantasy.[168]

Card cites the Book of Mormon as an important influence on his writing; his habit of beginning sentences with conjunctions comes from the book.[169] Literary devices in Hot Sleep parallel those of the book of mormon.[170] Collings said Hot Sleep's mimicry of Book of Mormon language makes it an "inherently" Mormon novel. Card combined several Worthing stories and revised Hot Sleep to create The Worthing Chronicle, which does not mirror the language of the Book of Mormon as much as Hot Sleep does.[171]

Themes[edit]
Child-genius savior[edit]
one theme in card's works is that of a precocious child who is isolated from others but is uniquely positioned to help or save their community. these characters with exceptional abilities achieve their destiny "through discipline and suffering".[172] Often, his gifted protagonists are introspective children.[173] Card's work features children and adults working together, which is unusual.[166] his characters feel "real" and must grow and take on responsibilities, and often sacrifice themselves to improve their own societies.[162] This sacrifice is a difficult choice in which none of the options are obviously good.[174] These protagonists have unusual abilities that are both a blessing and a curse. The protagonists, who are isolated from family and friends, relate better to adults than to other young people; when they grow up, they often mentor other precocious youths.[175][176] Alvin Maker follows this pattern; his magical abilities are very unusual and he uses them to redeem his people.[143]

according to collings, card's protagonists are "lonely and manipulative messiah-figures" who make sacrifices that can be interpreted as a declaration of principles. family and community problems arise when individuals are not fully accepted or when communities do not work with others in larger units.[177][51] Often one group tries to kill or enslave another group but their conflict is alleviated when they try to understand each other.[178] Protagonists make choices that save a person or a group of people.[174] In The Porcelain Salamander, a girl is saved by a magical salamander; this action restores her ability to move but she takes on some attributes of the salamander.[179] In Kingsmeat the Shepherd painlessly excises meat from humans to save them from being completely eaten by their alien overlords. The violence of removing parts of people is like the violence of repentance.[180] collings states part of this story "could serve as an epigram of all card's fictions; trapped within a circle of opposing forces, one focal character must decide whether or not to become, like ender wiggin, 'something of a savior, or a prophet, or at least a martyr' ."[181]

The original short story ender's Game is reminiscent of Heinlein's young adult novels because it is about a young person with impressive gifts who is guided by a stern mentor whose choices affect all of humanity.[165] The situations and choices in the Ender series invoke a number of philosophical topics, including the rules of war, embodiment psychology, the ethics of anthropology and xenology, and the morality of manipulating children.[182] Though Card described Happy Head (1978) as an embarrassment, it anticipated cyberpunk fiction with an investigator judge who can experience memories with witnesses. Both A Thousand Deaths (1978) and Unaccompanied Sonata feature protagonists who rebel against the dystopias they inhabit.[183]

American politics[edit]
In a May 2013 essay called "Unlikely Events", which Card presented as an experiment in fiction-writing,[184] Card described an alternative future in which President barack obama ruled as a "Hitler- or Stalin-style dictator" with his own national police force of young unemployed men; Obama and his wife Michelle would have amended the U.S. Constitution to allow presidents to remain in power for life, as in Nigeria, Zimbabwe, and Nazi Germany.[185][186] In the essay, first published in The Rhinoceros Times, Card attributed Obama's success to being a "black man who talks like a white man (that's what they mean by calling him "articulate" and a "great speaker")."[187]: 66  The essay drew criticism from journalists for its allusions to Obama's race and its reference to "urban gangs".[188][189][190] Vice author Dave Schilling featured the article in his "This Week in Racism" roundup several months after its publication.[191]

Empire (2006) is a novel about civil war between progressive and conservative extremists in America. It was a finalist for the Prometheus Award, an award given by the Libertarian Futurist Society.[192] Publishers Weekly stated that "right-wing rhetoric trumps the logic of story and character" in the novel.[193] Another review from Publishers Weekly noted that "Card's conservative bias seeps into" the novel.[194] At SFReviews, Thomas Wagner took further issue with Card's tendency to "smugly pretend[...] to be above it all," or claiming to be moderate while espousing conservative views of news media.[195] In an interview with Mythaxis Review in April 2021, Card stated that he writes fiction "without conscious agenda."[196]

Homosexuality[edit]
in card's fiction writing, homosexual characters appear in contexts that some critics have interpreted as homophobic. writing for Salon, Aja Romano lists the "homophobic subtext"[197] of characters in four of card's books. in Songmaster, a man falls in love with a 15-year-old castrato in a pederastic society. Their sexual union has "creepy overtones" that makes the teenager "unable to have sex again."[197] On the topic of Songmaster, Card wrote that he was not trying to show homosexual sex as beautiful. Romano wrote that the book's "main plot point revolve[d] around punishing homosexual sex."[197] in the homecoming series, a gay male character, zdorab, marries and procreates for the good of society. romano notes that zdorab does not stop being gay after his marriage, but that procreation is paramount in the book's society. eugene england defends zdorab, arguing that he is a sympathetic character who discovered that his homosexuality was determined by his mother's hormone levels during pregnancy. therefore, card acknowledges that homosexuality is not a character trait that can be erased or reversed. while zdorab marries and has children, he sees his choice to become a father as very deliberate and not "out of some inborn instinct."[198]

Card's 2008 novella hamlet's Father re-imagines the backstory of Shakespeare's play Hamlet. In the novella, Hamlet's friends were sexually abused as children by his pedophilic father and subsequently identify as homosexual adults. The novella prompted public outcry and its publishers were inundated with complaints.[199][200] Trade journal Publishers Weekly criticized Card's work, stating its main purpose was to attempt to link homosexuality with pedophilia.[201] card responded that he did not link homosexuality with pedophilia, stating that in his book, hamlet's Father was a pedophile that shows no sexual attraction to adults of either sex.[202]

Views[edit]
Politics[edit]
Card became a member of the U.S. Democratic Party in 1976 and has on multiple occasions referred to himself as a Moynihan or Blue Dog Democrat, as recently as 2020.[156][203] [204]: 0:58:09  Card supported Republican presidential candidate John McCain in 2008[205] and Newt Gingrich in 2012.[206] In 2016 he followed the "hold your nose, vote Trump" hashtag and voted accordingly.[204]: 1:01:10  According to Salon, Card's views are close to neoconservative.[197] Card has described himself as a moral conservative,[207][156] Card was a vocal supporter of the U.S.'s War on Terror.[208][209] In a 2020 interview with Ben Shapiro, Card stated that he was not a conservative because he has beliefs that do not align with typical conservative platforms, including desiring liberal immigration laws, gun control, and abolishing the death penalty.[204]: 0:58:49  In 2000, Card said he believed government has a duty to protect citizens from capitalism.[210]

Homosexuality[edit]
Card has publicly declared his support of laws against homosexual activity and same-sex marriage.[197][211] Card's 1990 essay "A Changed Man: The Hypocrites of Homosexuality" was first published in Sunstone[212] and republished in his collection of non-fiction essays, A Storyteller in Zion.[213] In the essay, he argued that laws against homosexual behavior should not be "indiscriminately enforced against anyone who happens to be caught violating them, but [used only] when necessary to send a clear message [to] those who flagrantly violate society's regulation". Card also questioned in a 2004 column the notion that homosexuality was a purely innate or genetic trait, and asserted that a range of environmental factors also contributed to its development, including abuse.[214] However, in an introduction to a reprint of his essay, Card wrote that since 2003, when the US Supreme Court had ruled those laws unconstitutional, he has "no interest in criminalizing homosexual acts".[215]

Card has stated there is no need to legalize same-sex marriage and that he opposes efforts to do so.[214] In 2008, he wrote in an opinion piece in the Deseret News that relationships between same-sex couples would always be different from those between opposite-sex couples, and that if a government were to say otherwise, "married people" would "act to destroy" it as their "mortal enemy".[216][217] In 2012, Card supported North Carolina Amendment 1, a ballot meaSure to outlaw same-sex marriage in north carolina, saying the legalization of gay marriage was a slippery slope upon which the political left would make it "illegal to teach traditional values in the schools".[218] In 2009, Card joined the board of directors of the National Organization for Marriage, a group that campaigns against same-sex marriage.[219] Card resigned from the board in mid-2013.[220] In July 2013, one week after the U.S. Supreme Court issued rulings in two cases that were widely interpreted as favoring recognition of same-sex marriages, Card published in Entertainment Weekly a statement saying the same-sex marriage issue is moot because of the Supreme Court's decision on the Defense of Marriage Act (DOMA).[221]

Card's views have had professional repercussions. In 2013, he was selected as a guest author for DC Comics' new Adventures of Superman comic book series,[222] but controversy over his views on homosexuality led illustrator Chris Sprouse to leave the project. An online petition to drop the story received over 16,000 signatures and DC Comics put Card's story on hold indefinitely.[223][224] A few months later, an LGBT non-profit organization[225] Geeks OUT proposed a boycott of the movie adaptation of ender's Game, calling Card's views "anti-gay"[226][227] and causing the movie studio Lionsgate to publicly distance itself from Card's opinions.[228]

Awards and legacy[edit]
Card won the ALA Margaret Edwards Award, which recognizes one writer and a particular body of work for "significant and lasting contributions to young adult literature",[229] in 2008 for his contribution in writing for teenagers; his work was selected by a panel of YA librarians.[230] card said he was unSure his work was suitable for the award because it was never marketed as "young adult".[231] In the same year, Card won the Lifetime Achievement Award for Mormon writers at the Whitney Awards.[232]

In 1978, the Harold B. Lee Library acquired the Orson Scott Card papers, which include Card's works, writing notes, and letters. The collection was formally opened in 2007.[233][234][235] Stephenie Meyer, Brandon Sanderson, and Dave Wolverton have cited Card's works as a major influence.[236][237][238] In addition, Card inspired Lindsay Ellis's novel Axiom's End.[239]

Card has also won numerous awards for single works:

1978 John W. Campbell Award for Best New Writer from the World Science Fiction Convention, citing the ender's Game novelette[51]
1984 Saints: Book of the Year by the Association for Mormon Letters[240]
1985 ender's Game: Nebula Award, 1985;[241] Hugo Award, 1986;[242]
1986 speaker for the Dead; Nebula Award, 1986,[242] Hugo Award, 1987;[243] Locus Award, 1987;[242] SF Chronicle Readers Poll Award 87[244]
1987 "Eye for Eye": Hugo Award, 1988;[245] Seiun Award, 1989[246]
1987 "Hatrack River": nebula nominee, 1986,[247] Hugo nominee, 1987,[248] World Fantasy Award (WFA) winner - novella, 1987[249]
1988 seventh Son: Hugo and WFA nominee, 1988;[250] Mythopoeic Society Award 1988;[251] Locus Award winner, 1988[250]
1989 red Prophet: Hugo nominee, 1988;[250] Nebula Nominee, 1989;[252] Locus winner, 1989[252]
1991 how to Write Science Fiction and Fantasy (Writer's Digest Books, 90): Hugo Award[253]
1995 alvin Journeyman: Locus Award winner, 1996[254]
2002 shadow of the Hegemon: ALA Best Books for Young Adults[255]
Other activities[edit]
Since 1994, Card has served as a judge for Writers of the Future, a science fiction and fantasy story contest for amateur writers.[256] In late 2005, Card launched Orson Scott Card's InterGalactic Medicine Show, an online fantasy and science fiction magazine.[257] In 2005, Card accepted a permanent appointment as "distinguished professor" at Southern Virginia University in Buena Vista, Virginia, a small liberal arts college.[258] Card has served on the boards of a number of organizations, including public television station UNC-TV (2013–present)[259] and the National Organization for Marriage (2009–2013).[260]

Card taught a course on novel-writing at Pepperdine University, which was sponsored by Michael Collings. Afterwards, Card designed his own writing courses called "Uncle Orson's Writing Course" and "literary boot camp".[9] Eric James Stone, Jamie Ford, Brian McClellan, Mette Ivie Harrison and John Brown have attended Card's literary boot camp.[261] Luc Reid, founder of the Codex Writers Group is also a literary book camp alumnus.[262] Card has been a Special Guest and/or Literary Guest of Honor and Keynote Speaker at the Life, the Universe, & Everything professional science fiction and fantasy arts symposium, on at least six separate occasions: 1983, 1986, 1987, 1997, 2008, 2014.[263]

See also[edit]
￼	Children's literature portal
￼
Speculative fiction portal
￼	Biography portal
Orson Scott Card bibliography
LDS fiction
Descendants of Brigham Young
References[edit]
^ Jump up to:a b c Card, Orson Scott (1990). maps in a Mirror: The Short Fiction of Orson Scott Card. New York: ORB. ISBN 9780765308405. Retrieved September 30, 2019.
^ Tyson 2003, p. 165.
^ Willett 2006, p. 77.
^ Willett 2006, p. 13.
^ Jump up to:a b c Tyson 2003, p. xv.
^ Jump up to:a b Tyson 2003, p. xvi.
^ Card, Orson Scott. "About Orson Scott Card".
^ Willett 2006, pp. 36–37.
^ Jump up to:a b c d e Card, Orson Scott. "Why I am Teaching at SVU... and Why SVU is Important". Meridian Magazine. Archived from the original on October 21, 2013.
^ "Orson Scott Card and Rod McKuen and poetry". Poetry Foundation. Retrieved September 25, 2019.
^ Tyson 2003, p. xxi; 166.
^ Jump up to:a b c Tyson 2003, p. xvii.
^ "Orson Scott Card". The Washington Post. November 3, 2010. Retrieved September 25, 2019.
^ Groeger, Gina (November 13, 2000). "Orson Scott Card visits BYU". The Daily Universe. Brigham Young University. Retrieved September 25, 2019.
^ Willett 2006, pp. 38–42.
^ Van Name 1988, p. 3.
^ Willett 2006, pp. 41–43.
^ Jump up to:a b Tyson 2003, p. xx.
^ Tyson 2003, p. 166.
^ Jump up to:a b c "Orson Scott Card (Louie Free - Brain Food from the Heartland)". Vindy Archives. January 18, 2019.
^ Jump up to:a b Manier, Terry (October 31, 2013). "orson scott card talks ender's Game in rare interview". Wired. Retrieved September 26, 2019.
^ Tyson 2003, pp. xx–xxi.
^ "Posing as People". Hatrack River enterprises inc.
^ Locus Publications (January 5, 2011). "Locus Online News » Orson Scott Card Suffers Mild Stroke". Locusmag.com. Retrieved March 14, 2013.
^ Willett 2006, p. 43.
^ Hall, Andrew (April 8, 2017). "Lifetime Achievement Awards: Orson Scott Card and Susan Elizabeth Howe". Dawning of a Brighter Day: Twenty-First Century Mormon Literature. Association for Mormon Letters. Retrieved September 27, 2019.
^ Collings, Michael R. (1990). in the image of god: theme, characterization, and landscape in the fiction of orson scott card. Westport, Connecticut: Greenwood Press. ISBN 031326404X.
^ Van Name 1988, p. 5.
^ Van Name 1988, p. 2; 5.
^ Van Name 1988, p. 2–4.
^ Willett 2006, pp. 42–43.
^ Willett 2006, pp. 43, 48.
^ Jump up to:a b Lupoff 1991, p. 121.
^ Collings 2001, pp. 12, 292–294.
^ Willett 2006, p. 56.
^ "1979 Hugo Awards". The Hugo Awards. July 26, 2007. Retrieved February 18, 2020.
^ "sfadb: Nebula Awards 1979". www.sfadb.com. Retrieved February 18, 2020.
^ Willett 2006, pp. 48–49.
^ "Nebula Awards 1980". Science Fiction Awards Database. Locus. Archived from the original on October 25, 2015. Retrieved December 6, 2011.
^ "1980 Hugo Awards". World Science Fiction Society. July 26, 2007. Archived from the original on May 7, 2011. Retrieved April 19, 2010.
^ Jump up to:a b Collings 2001, p. 13.
^ Willett 2006, p. 47.
^ Collings 2001, p. 12.
^ Willett 2006, pp. 51–52.
^ Willett 2006, p. 54.
^ Jump up to:a b c "Orson Scott Card: Jack of Many Trades". Locus. 20 (6): 56–58. June 1987.
^ Willett 2006, p. 60–61.
^ Willett 2006, pp. 62–63.
^ Westfahl 1998, p. 182–183.
^ "Winner of the Hugo and Nebula Awards". Nebula Awards. Science Fiction and Fantasy Writers of America. Retrieved September 26, 2019.
^ Jump up to:a b c d e f g Clute, John. "Card, Orson Scott". In Clute, John; Langford, David; Nicholls, Peter; Sleight, Graham (eds.). Encyclopedia of Science Fiction (3rd ed.). SFE.
^ Willett 2006, p. 96.
^ "Program Information - Bobs Slacktime Funhouse: BSTF 917 - Orson Scott Card's Secular Humanist Revival Meeting". www.radio4all.net.
^ Card, Orson Scott. "The secular, humanist revival meeting". search.lib.byu.edu.
^ "1988 Hugo Awards". World Science Fiction Society. Archived from the original on May 7, 2011. Retrieved April 19, 2010.
^ Collings 2001, p. 15.
^ Card, Orson Scott; Van Name, Mark L. "Short Form". search.lib.byu.edu.
^ Jump up to:a b c Collings 2001, pp. 15–16.
^ Scott, Orson (1991). "Interview". Leading Edge. No. 23. Brigham Young University.
^ Gates, Crawford. "The Delights of Making Cumorah's Music". Maxwell Institute. Journal of Book of Mormon Studies. Archived from the original on April 7, 2007.
^ Jump up to:a b c Oziewicz 2008, p. 209.
^ Jump up to:a b Collings 2014, p. 32.
^ England 1990, p. 57.
^ "The Mythopoeic Society: Mythopoeic Fantasy Award Finalists". www.mythsoc.org.
^ "The Mythopoeic Society: Mythopoeic Awards". www.mythsoc.org.
^ Oziewicz 2008, p. 205.
^ England 1990, p. 58; 62.
^ Tyson 2003, p. xxi; 33.
^ Ling, Van (September 24, 1989). "A Response Rising Out of "The Abyss"". los Angeles times. Retrieved October 1, 2019.
^ Westfahl 1998, p. 183–184.
^ England 1994, p. 59.
^ Collings 2001, pp. 16–17.
^ "1996 Award Winners & Nominees". Worlds Without End. Retrieved October 20, 2020.
^ "1999 Awards Winners & Nominees". Worlds Without End.
^ Collings 2014, p. 362.
^ Linder, Brian (June 17, 2012). "doug chiang's Robota". IGN. Retrieved September 26, 2019.
^ Hall, Andrew (December 17, 2015). "In Memoriam: Kathryn H. Kidd". Dawning of a Brighter Day: Twenty-First Century Mormon Literature. Association of Mormon Letters. Retrieved September 26, 2019.
^ Tyson 2003, pp. 125–127.
^ Collings 2001, pp. 263–267, 273–275.
^ Tyson 2003, pp. 127–135.
^ Peterson, Matthew (November 12, 2009). "Orson Scott Card - Online Radio Interview with the Author". The Author Hour radio show.
^ Card, Orson (April 5, 2020). "Maybe Some Good Will Come Out of This". Hatrack River. Retrieved August 18, 2020.
^ Lythgoe, Dennis (December 16, 2007). "book review: "a War of Gifts: an ender story"". Deseret News. Deseret News Publishing Company. Retrieved September 26, 2019.
^ Collings 2014, p. 197.
^ "Formic Wars: Silent Strike". www.aaronwjohnston.com. February 3, 2016.
^ "Formic Wars: Burning Earth (2011)". Marvel Entertainment.
^ "Formic Wars: Silent Strike (2011 - 2012)". Marvel Entertainment.
^ Jump up to:a b Card, Orson Scott; Johnston, Aaron (2012). earth Unaware: the first formic war. New York: Tor. pp. 366–368. ISBN 9780765329042.
^ Jump up to:a b c Card, Orson Scott. "The Library of Orson Scott Card". www.hatrack.com. Retrieved February 25, 2020.
^ Bowyer, Jerry (November 17, 2017). "children of the Fleet: orson scott card's best since ender's Game". Forbes. Retrieved September 26, 2019.
^ Tyson 2003, pp. 79–94.
^ "subterranean press space Boy". subterraneanpress.com. Retrieved February 26, 2020.
^ card, orson scott (2008). "hamlet's Father". in kaye, marvin (ed.). The Ghost Quartet. New York: TOR. ISBN 9780765312518. Retrieved September 27, 2019.
^ "orson scott card: stonefather". www.sfsite.com. The SF Site.
^ "Mither Mages Series by Orson Scott Card". www.goodreads.com.
^ Card, Orson Scott (November 3, 2015). pathfinder trilogy. ISBN 9781481457729. Retrieved February 25, 2020.
^ Haley, Carolyn. "lost and Found". www.nyjournalofbooks.com.
^ Card, Orson Scott (2005). catalog record for magic Street. Harold B. Lee Library. ISBN 9780345416896.
^ Card, Orson Scott (November 2, 2008), Uncle Orson Reviews Everything: Bean on Baseball and Parker's Trilogies, Hatrack River enterprises inc, retrieved March 28, 2011
^ Collings, Michael (November 6, 2018). "Book review: Orson Scott Card's new book is a Hallmark Christmas movie in prose, but better". Deseret News.
^ "invasive Procedures". www.publishersweekly.com. Retrieved February 26, 2020.
^ "Interview with Author Orson Scott Card". Gaming Today. Archived from the original on June 20, 2007. Retrieved June 18, 2007.
^ "NeoHunter (1996)". MobyGames. Retrieved February 20, 2020.
^ Vitka, William (January 25, 2005). "Game Preview: Advent Rising". CBS News. CBS Interactive. Retrieved September 27, 2019.
^ Weiss, Danny (June 23, 2005). "Video Game Review: "Advent Rising"". NBC News. NBCNews. Retrieved September 27, 2019.
^ Castro, Adam-Troy (December 14, 2012). "We Preview Shadow Complex: Best Game of Summer?". Syfy Wire. Syfy. Retrieved September 26, 2019.
^ "Shadow Complex Xbox 360 Video - Dev. Diary". IGN Video. Archived from the original on August 17, 2009.
^ Willett 2006, p. 84.
^ Haddock, Marc (October 17, 2011). "Book review: Orson Scott Card teams up with his daughter to create 'Laddertop'". Deseret News.
^ "Comics Book Review: Laddertop, Vol. 1 by Orson Scott Card, Emily Janice Card, Zina Card and Honoel A. Ibardolaza. Tor/Seven Seas, $10.99 trade paper (192p) ISBN 978-0-7653-2460-3". PublishersWeekly.com.
^ Johnston, Aaron (February 4, 2016). "Dragon Age". www.aaronwjohnston.com. Retrieved February 25, 2020.
^ Scribner, Herb (January 5, 2018). "BYUtv's sci-fi series "Extinct" won't be renewed for a second season". Deseret News. Deseret News Publishing Company. Retrieved September 24, 2019.
^ "BYUtv taps anti-gay Orson Scott Card to create, write, produce its new scripted series". The Salt Lake Tribune. September 15, 2016. Retrieved October 4, 2019.
^ "ender's Game hits comics - ign".
^ Johnston, Aaron. "Graphic Novels". www.aaronwjohnston.com. Retrieved February 25, 2020.
^ Ekstrom, Steve (October 6, 2008). "Chris Yost: Bringing Ender Wiggin to Comics". newsarama. Retrieved February 26, 2020.
^ Card, Orson Scott (2013). "catalog record for ender's Game". search.lib.byu.edu. Harold B. Lee Library. Retrieved February 26, 2020.
^ Card, Orson Scott (2012). "Catalog record for Ender's shadow ultimate collection". search.lib.byu.edu. Harold B. Lee Library.
^ "gcd :: issue :: ender's Game: War of Gifts". www.comics.org. Grand Comics Database. Retrieved February 26, 2020.
^ "ender's Game: mazer in prison (now available)". www.aaronwjohnston.com. March 21, 2010. Retrieved February 26, 2020.
^ "enders game War of Gifts (2009 marvel) comic books". www.mycomicshop.com. Retrieved February 26, 2020.
^ Peterson, Jeff (November 4, 2013). ""ender's Game" movie was worth the wait". Deseret News. Deseret News Publishing Company. Retrieved September 26, 2019.
^ Lawrence, Bryce (July 16, 2013). "orson scott card: praise for work of "ender's Game" director, movie executives". The Daily Universe. Brigham Young University. Retrieved September 26, 2019.
^ "Movie production team being assembled". Taleswapper, Inc. February 25, 2009. Retrieved March 1, 2009.
^ McNary, Dave (April 28, 2011). "summit plays 'ender's Game'". Variety.
^ Snow, Shane. "orson scott card talks ender's Game in rare interview". Wired. Retrieved November 1, 2013.
^ Zeitchik, Steven (September 20, 2010). "gavin hood looks to play 'ender's Game'". los Angeles times.
^ "critics, community and "ender's Game": an interview with orson scott card". Deseret News. Deseret News Publishing Company. October 31, 2013. Retrieved October 4, 2019.
^ Lawrence, Bryce (July 16, 2013). "orson scott card: praise for work of 'ender's Game' director". The Digital Universe. Brigham Young University. Archived from the original on July 18, 2013.
^ "ender's Game (2013)". Rotten Tomatoes. Fandango Media. Retrieved May 4, 2020.
^ Hall, Andrew (November 9, 2013). "This Week in Mormon Literature, November 9, 2013". Dawning of a Brighter Day: Twenty-First Century Mormon Literature. Association of Mormon Letters. Retrieved September 26, 2019.
^ Card, Orson Scott. "World Watch". www.ornery.org. The Ornery American.
^ Buckley, Bob (April 30, 2013). "The Rhinoceros Times going out of business after 20 years". Fox 8. Retrieved September 26, 2019.
^ "Search for "uncle orson"". The Rhino Times of Greensboro.
^ Card, Orson Scott. "Uncle Orson Reviews Everything". Hatrick River: The Official Website of Orson Scott Card. Hatrack River enterprises. Retrieved September 26, 2019.
^ "Nauvoo Times - Orson%20Scott%20Card". www.nauvootimes.com. Retrieved February 26, 2020.
^ Willett 2006, p. 19–21.
^ Willett 2006, p. 20.
^ Jump up to:a b Collings 2014, p. 31.
^ drinkin' bros podcast #617 - ender's Game series author orson scott card, archived from the original on December 19, 2021, retrieved November 14, 2021
^ Collings 2014, p. 24.
^ Card, Orson Scott (Summer 2013). "A Brief Interview with Orson Scott Card (extended answers)". Tor. p. 2:45. Archived from the original on December 19, 2021. Retrieved November 20, 2020.
^ Jump up to:a b Samuelson 1996, p. 912.
^ Willett 2006, pp. 12–15, 95.
^ Collings 2014, p. 18.
^ "Reid, Suzanne Elizabeth 1944- | Encyclopedia.com". www.encyclopedia.com.
^ Collings 2014, p. 38.
^ Reid 1998, p. 50; 37.
^ Jump up to:a b Collings 2014, pp. 55–57.
^ Collings 2014, pp. 57–58.
^ Collings 2001, p. 11.
^ Collings 2014, pp. 67, 69.
^ Smith 2011, p. 54.
^ Collings 2014, p. 72.
^ Collings 2014, p. 85.
^ Jump up to:a b c Askar, Jamshid Ghazi (October 31, 2013). "critics, community and 'ender's Game': an interview with orson scott card". Deseret News.
^ England 1994, pp. 59–61.
^ Smith 2011, pp. 54–56.
^ England 1994, pp. 70–71.
^ Westfahl 1998, p. 185.
^ Reid 1998, p. 50.
^ Jump up to:a b c Bleiler 1989, p. 134–135.
^ Westfahl 2005, p. 197.
^ Nicol 1992, p. 130.
^ Jump up to:a b Westfahl 1998, pp. 181–182.
^ Jump up to:a b Westfahl 1998, p. 179.
^ Collings 2014, pp. 22–23.
^ Tyson 2003, pp. 160–161.
^ Willett 2006, p. 22.
^ Collings 2014, pp. 61–63.
^ Collings 2014, pp. 64, 67.
^ Beswick 1989, p. 52.
^ Lupoff 1991, pp. 120–121.
^ Jump up to:a b Tyson 2003, p. 157.
^ Tyson 2003, p. 158.
^ Collings 2014, p. 15.
^ Collings 2014, p. 94.
^ Tyson 2003, pp. 159–160.
^ Collings 2014, p. 95–96.
^ Collings 2014, p. 96–98.
^ Collings 2014, p. 36.
^ WittkowerRush 2013, p. 35; 48; 65; 112.
^ Westfahl 1998, p. 180.
^ Card, Orson Scott (May 9, 2013). "Unlikely Events". The Ornery American. Archived from the original on June 8, 2013. Retrieved November 2, 2016.
^ Child, Ben (August 16, 2013). "ender's Game author orson scott card compares obama to hitler". The Guardian.
^ Horn, John (August 15, 2013). "'ender's Game' author compares obama to hitler". los Angeles times.
^ Card, Orson Scott (May 16, 2013). "Civilization Watch: Unlikely Events". The Rhinoceros Times. Retrieved December 14, 2020.
^ Florien, Daniel (August 16, 2013). "Orson Scott Card's Alternate Future". Patheos.
^ Waldman, Paul (August 16, 2013). "Morally Compromised Art, on the Big Screen: How do we judge a movie made from a book written by someone with repellent political views?". The American Prospect.
^ "Controversial author Orson Scott Card named to UNC-TV board". Winston-Salem Journal. Associated Press. September 9, 2013.
^ Schilling, Dave (August 16, 2013). "Orson Scott Card Is Officially the Most Racist Sci-Fi Author". www.vice.com.
^ "Libertarian Futurist Society". lfs.org. Archived from the original on September 19, 2020. Retrieved November 30, 2020.
^ "fiction book review: Empire by Orson Scott Card". PublishersWeekly.com. November 2006. Retrieved November 30, 2020.
^ Card, Orson Scott (2006). Empire by Orson Scott Card. Harold B. Lee Library. ISBN 9780765316110.
^ "Empire / Orson Scott Card ☆☆". www.sfreviews.net. Retrieved November 30, 2020.
^ Smistad, John (April 18, 2021). "ender's Game and beyond: an interview with orson scott card". Mythaxis Review.
^ Jump up to:a b c d e Romano, Aja (May 8, 2013). "Orson Scott Card's long history of homophobia". Salon. Retrieved November 9, 2020.
^ England, Eugene (1994). "Dawning of a Brighter Day". Sunstone.
^ Flood, Alison. "Outcry over Hamlet novel casting old king as gay pedophile: Publisher showered with complaints over Orson Scott Card's hamlet's Father" The Guardian 8 September 2011
^ "osc responds to false statements about hamlet's Father (Orson Scott Card) – September 2011". Hatrack.com. Retrieved March 14, 2013.
^ "review of hamlet's Father". Publishersweekly.com. February 28, 2011. Retrieved March 14, 2013.
^ Card, Orson Scott. "osc responds to false statements about hamlet's Father". www.hatrack.com. Retrieved November 15, 2021.
^ Card, Orson Scott (September 6, 2012). "Premium Rush, 50 Things, Deadly Animals, Harbach". Rhinoceros Times.
^ Jump up to:a b c Shapiro, Ben (May 24, 2020). "The Ben Shapiro Show Sunday Special Ep. 96". The Daily Wire. Archived from the original on December 19, 2021.
^ Card (November 4, 2008). "WorldWatch – This Very Good Election Year – The Ornery American". Ornery.org. Archived from the original on June 29, 2017. Retrieved July 10, 2010.
^ Card (December 1, 2011). "Hugo, Scorsese, Romney, and Gingrich". Uncle Orson Reviews Everything. Hatrack.com.
^ Card (December 20, 2009). "worldwatch - sarah palin's book - the ornery american". Ornery.org. Retrieved March 14, 2013.
^ Card, Orson Scott (November 6, 2006). "The Only Issue This Election Day". RealClearPolitics from Rhinoceros Times.
^ Card, Orson Scott (January 15, 2006). "Iraq -- Quit or Stay?". Rhinoceros Times.
^ Minkowitz, Donna (February 3, 2000). "My favorite author, my worst interview: I worshipped militaristic Mormon science-fiction writer Orson Scott Card -- until we met". Salon.
^ "NYC-based group calls for boycott of sci-fi movie over author's gay rights views". CBS New York. July 9, 2013.
^ Card, Orson Scott (February 1990). "A Changed Man: The Hypocrites of Homosexuality" (PDF). Sunstone Magazine: 44–45. Retrieved June 16, 2017.
^ England 1994, p. 71.
^ Jump up to:a b Card, Orson Scott. "Homosexual "Marriage" and Civilization". The Ornery American. Archived from the original on February 24, 2004. Retrieved November 16, 2016.
^ Card, Orson Scott. "The Hypocrites of Homosexuality - Orson Scott Card". www.nauvoo.com.
^ Quinn, Annalisa (July 10, 2013). "book news: 'ender's Game' author responds to boycott threats". NPR.
^ Card, Orson Scott (July 24, 2008). "Orson Scott Card: State job is not to redefine marriage". The Deseret News. Retrieved November 16, 2016.
^ Staff Reports (May 7, 2012). "Author: Marriage amendment is about forcing 'anti-religious values' on children". LGBTQ Nation. Retrieved January 27, 2020.
^ Romano, Aja (May 7, 2013). "orson scott card's long history of homophobia: in honor of the "ender's Game" trailer release, a look at some of the sci-fi master's most controversial remarks". Salon.
^ Cieply, Michael (July 12, 2013). "Author's Views on Gay Marriage Fuel Call for Boycott". The New York Times.
^ Lee, Stephan (July 8, 2013). "'ender's Game' author answers critics: gay marriage issue is 'moot'". Entertainment Weekly. Retrieved November 17, 2021.
^ Peeples, Jase (February 12, 2013). "DC Comics Responds to Backlash Over Hiring Antigay Writer". The Advocate. Retrieved February 13, 2013.
^ Truitt, Brian (March 5, 2013). "Artist leaves Orson Scott Card's Superman comic". USA Today. Retrieved March 15, 2013.
^ McMillan, Graeme (March 5, 2013). "Orson Scott Card's Controversial Superman Story Put on Hold". Wired.com. Retrieved May 3, 2013.
^ "Geeks OUT". Geeks OUT. Retrieved January 23, 2020.
^ Child, Ben (July 9, 2013). "activists call for ender's Game boycott over author's anti-gay views". The Guardian. London.
^ Kellogg, Carolyn (July 11, 2013). "orson scott card's antigay views prompt 'ender's Game' boycott". los Angeles times. Retrieved July 20, 2013.
^ Cheney, Alexandra (July 12, 2013). "studio comes out against 'ender's Game' author on gay rights". The Wall Street Journal.
^ "Margaret A. Edwards Award". American Library Association. Retrieved September 24, 2019.
^ "Orson Scott Card honored for lifetime contribution to young adult readers with Edwards Award". American Library Association. March 17, 2008. Retrieved September 24, 2019.
^ "Looking Back". YALSA. ALA. Retrieved 2013-10-13. Card won the 20th anniversary Edwards Award in 2008, when YALSA asked previous winners to reflect on the experience. Some live remarks by Card are published online with the compiled reflections but transcripts of acceptance speeches are available to members only.
^ "Orson Scott Card's Whitney Award Speech". Mormontimes.com. Archived from the original on May 1, 2009. Retrieved March 14, 2013.
^ Orson Scott Card Papers 1966-(ongoing)
^ Peterson, Janice (September 13, 2007). "Author makes living with 'lies'". Daily Herald. Retrieved March 17, 2016.
^ "Orson Scott Card 1951-present". Literary Worlds: Illumination of the Mind. Archived from the original on 2 March 2016. Retrieved 17 March 2016.
^ Nevarez, Lisa A., ed. (2013). The Vampire Goes to College : Essays on Teaching With the Undead. McFarland. p. 145. ISBN 978-0786475544.
^ "About Brandon". Brandon Sanderson. November 23, 2019. Retrieved February 20, 2020.
^ Dodge. (December 10, 2003). "An Interview with the author David Wolverton". wotmania. Archived from the original on May 26, 2006.
^ Rouner, Jef (July 21, 2020). "In YouTube star's debut novel, Bush administration bungles alien contact". San Francisco Chronicle. Retrieved July 31, 2020.
^ "1984 AML Awards". Association for Mormon Letters. Retrieved July 14, 2009.
^ "1985 Award Winners & Nominees". Worlds Without End. Retrieved July 15, 2009.
^ Jump up to:a b c "1986 Award Winners & Nominees". Worlds Without End. Retrieved July 15, 2009.
^ "1987 Award Winners & Nominees". Worlds Without End. Archived from the original on June 13, 2020. Retrieved July 15, 2009.
^ "Science Fiction Chronicle Readers Poll 1987". Science Fiction Awards Database. Locus Science Fiction Foundation. Retrieved September 24, 2019.
^ "1988 Hugo Awards". The Hugo Awards. July 26, 2007. Retrieved September 24, 2019.
^ "星雲賞受賞作・参考候補作一覧" [List of The Seiun Awards Winners & Candidates] (in Japanese). Retrieved March 25, 2016.
^ "Hatrack River". Nebula Awards. Science Fiction & Fantasy Writers of America. Retrieved September 24, 2019.
^ Walton, Jo (June 12, 2011). "Hugo Nominees: 1987". TOR. Macmillan. Retrieved September 24, 2019.
^ "Winners". World Fantasy Convention. World Fantasy Conventions. Retrieved September 24, 2019.
^ Jump up to:a b c "1988 Award Winners & Nominees". Worlds Without End. Retrieved July 15, 2009.
^ "Winners". Mythopoeic Society. The Mythopoeic Society. Retrieved September 24, 2019.
^ Jump up to:a b "1989 Award Winners & Nominees". Worlds Without End. Retrieved July 15, 2009.
^ "1991 Hugo Awards". The Hugo Awards. July 26, 2007. Retrieved September 24, 2019.
^ "1996 Award Winners & Nominees". Worlds Without End. Retrieved July 15, 2009.
^ "shadow of the Hegemon". American Library Association. Retrieved September 26, 2019.
^ "Writer Judge — Biography". Retrieved January 28, 2020.
^ "Orson Scott Card's Intergalactic Medicine Show". Retrieved October 18, 2006.
^ Kidd, Kathryn H. (May 16, 2005). "Noted Author Joins SVU Faculty". Meridian Magazines. Retrieved September 27, 2019.
^ Fain, Travis (September 9, 2013). "Orson Scott Card named to UNC-TV board - News-Record.com: North State Politics". News-Record.com. Retrieved September 12, 2013.
^ Lapidos, Juliet (July 20, 2013). "the 'ender's Game' boycott". The New York Times.
^ Woodbury, Kathleen Dalton. "Hatrack River writers workshop". hatrack.com.
^ Card, Orson Scott. "Former Boot Campers Published". hatrack.com.
^ "Life, the Universe, & Everything 32: The Marion K. "Doc" Smith Symposium on Science Fiction and Fantasy" (PDF). LTUE Press. February 1, 2014.
Works cited[edit]
Beswick, Norman (1989). "Amblick and After: Aspects of Orson Scott Card". Foundation. 45 (Spring 1989).
Bleiler, Richard (1989). "Card, Orson Scott". In Fletcher, Marilyn P.; Thorson, James L. (eds.). Reader's Guide to Twentieth-Century Science Fiction. Chicago and London: American Library Association. ISBN 9780838905043.
Collings, Michael (2001). Storyteller: Orson Scott Card. Overlook Connection Press. ISBN 1892950499.
Collings, Michael R. (2014). Orson Scott Card: Penetrating to the Gentle Heart. CreateSpace. ISBN 978-1-4991-2412-5.
England, Eugene (1994). "Orson Scott Card: The Book of Mormon as History and Science Fiction". Review of Books on the Book of Mormon. 6 (2). Retrieved January 29, 2020.
england, eugene (1990). "orson scott card: how a great science fictionist uses the book of mormon reviewed work(s): the folk of the fringe. The Tales of Alvin Maker, including these volumes: seventh Son. the red Prophet. prentice alvin by orson scott card". Review of Books on the Book of Mormon. 2.
Lupoff, Richard A. (1991). "Card, Orson Scott". In Watson, Noelle; Schellinger, Paul E. (eds.). Twentieth-Century Science-Fiction Writers (3rd ed.). Chicago and London: St. James Press.
Nicol, Charles (March 1992). "Mormon and Mammon". Science Fiction Studies. 19 (1): 128–130. JSTOR 4240132.
Oziewicz, Marek (2008). One Earth, One People: The Mythopoeic Fantasy Series of Ursula K. Le Guin, Lloyd Alexander, Madeline L'Engle and Orson Scott Card. McFarland & Company, Inc. ISBN 9780786431359.
Reid, Suzanne Elizabeth (1998). "A New Master: Orson Scott Card". Presenting Young Adult Science Fiction. Twayne Publishers. ISBN 080571653X.
Smith, Christopher C. (March 2011). "Sacred Sci-Fi: Orson Scott Card as Mormon Mythmaker" (PDF). Sunstone.
samuelson, scott (1996). "The Tales of Alvin Maker". in shippey, t.a.; sobczak, a.j. (eds.). McGill's Guide to Science Fiction and Fantasy Literature. Vol. 4. Pasadena, CA: Salem Press Inc.
Tyson, Edith S. (2003). Orson Scott Card: Writer of the Terrible Choice. Lantham, Maryland: Scarecrow Press, Inc. ISBN 0810847906.
Van Name, Mark L. (1988). "Writer of the Year: Orson Scott Card". In Collins, Robert A.; Latham, Robert (eds.). Science Fiction & Fantasy Book Review Annual 1988. Westport: Meckler. ISBN 0887362494. Retrieved September 30, 2019.
Westfahl, Gary (1998). "Orson Scott Card". In Bleiler, Richard (ed.). Science Fiction Writers: Critical Studies of the Major Authors from the Early Nineteenth Century to the Present Day (Second ed.). Charles Scribner's Sons. ISBN 0684805936.
Westfahl, Gary (2005). "Hard Science Fiction". In Seed, David (ed.). A Companion to Science Fiction. ISBN 1405112182.
Willett, Edward (2006). Orson Scott Card: Architect of Alternate Worlds. Berkeley Heights, NJ: Enslow Publishers. ISBN 0766023540.
Wittkower, D.E.; Rush, Lucinda, eds. (2013). ender's Game and philosophy: genocide is child's play. Open Court. ISBN 9780812698343.
Further reading[edit]
Card Catalogue: The Science Fiction and Fantasy of Orson Scott Card, Michael R. Collings, Hypatia Press, 1987, ISBN 0-940841-01-0
The Work of Orson Scott Card: An Annotated Bibliography and Guide, Michael R. Collings and Boden Clarke, 1997
Storyteller: The Official Guide to the Works of Orson Scott Card, Michael R. Collings, Overlook Connection Press, 2001, ISBN 1-892950-26-X
Hillstrom, Kevin, ed. (2004). Biography Today: Authors Vol. 14 (PDF). Detroit, Michigan: Omnigraphics. ISBN 0780806522. Retrieved September 30, 2019.
Stout, W. Bryan (July 1, 1989). "seventh Son; red Prophet; prentice alvin orson scott card". BYU Studies Quarterly. 29 (3): 114. Retrieved September 26, 2019.
External links[edit]
￼
Wikiquote has quotations related to Orson Scott Card.
￼
Wikimedia Commons has media related to Orson Scott Card.
Library resources
By Orson Scott Card
Resources in your library
Resources in other libraries
Official website
Orson Scott Card at the Internet Book List
Orson Scott Card at the Internet Speculative Fiction Database
Orson Scott Card at the Encyclopedia of Science Fiction
Orson Scott Card at the Encyclopedia of Fantasy
Orson Scott Card at IMDb
Orson Scott Card at the MLCA Database
Orson Scott Card papers, MSS 1756 at L. Tom Perry Special Collections, Brigham Young University
Orson Scott Card exhibit, includes several scans of manuscript items from the Orson Scott Card papers at L. Tom Perry Special Collections, Brigham Young University
hidevte
Works by Orson Scott Card
show
ender's Game series
show
The Tales of Alvin Maker
show
The Worthing series
show
Other works
showvte
Hugo Award for Best Novel
showvte
Hugo Award for Best Novella
showvte
Nebula Award for Best Novel
showvte
World Fantasy Award—Novella
showvte
Locus Award for Best Science Fiction Novel
showvte
Locus Award for Best Fantasy Novel
showvte
Locus Award for Best Short Story
show
Authority control ￼
Categories: 1951 births20th-century American novelists20th-century Mormon missionaries21st-century American non-fiction writers21st-century American novelistsAmerican Latter Day Saint writersAmerican Mormon missionaries in BrazilAmerican children's writersAmerican comics writersAmerican fantasy writersAmerican male non-fiction writersAmerican male novelistsAmerican online publication editorsAmerican science fiction writersBrigham Young University alumniHugo Award-winning writersJohn W. Campbell Award for Best New Writer winnersLatter Day Saints from ArizonaLatter Day Saints from North CarolinaLatter Day Saints from UtahLatter Day Saints from Washington (state)Living peopleMargaret A. Edwards Award winnersMormon apologistsNational Organization for Marriage peopleNebula Award winnersNorth Carolina DemocratsWriters from North CarolinaNovelists from North CarolinaNovelists from UtahNovelists from VirginiaPeople from Richland, WashingtonSouthern Virginia University facultyUniversity of Notre Dame alumniUniversity of Utah alumniWashington (state) DemocratsWorld Fantasy Award-winning writersWriters from CaliforniaWriters from Greensboro, North CarolinaWriters of books about writing fictionWriters of young adult science fiction20th-century American male writers21st-century American male writersAmerican anti-same-sex-marriage activistsActivists from North CarolinaActivists from UtahActivists from VirginiaActivists from Washington (state)
This page was last edited on 25 January 2023, at 02:44 (UTC).
Text is available under the Creative Commons Attribution-ShareAlike License 3.0; additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.
Privacy policyAbout WikipediaDisclaimersContact WikipediaMobile viewDevelopersStatisticsCookie statement￼￼￼
one))
            else:
                break
    return ret
