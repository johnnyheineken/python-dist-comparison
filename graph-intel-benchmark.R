library(rjson)
library(tidyverse)
library(reshape2)
json_data <- fromJSON(file="/home/jan/Documents/aLook/blog/python-comparison/ibench-ouput/all-clean.out")$runs
clean <- c()
test_name <- c()
for (test in json_data) {
  test_name <- c(test_name, test$name)
  clean <- c(clean,test$stats$median)
}
df <- cbind.data.frame(test_name, clean)


json_data <- fromJSON(file="/home/jan/Documents/aLook/blog/python-comparison/ibench-ouput/all-conda.out")$runs
time <- c()
for (test in json_data) {
  time <- c(time,test$stats$median)
}
df$conda <- time

json_data <- fromJSON(file="/home/jan/Documents/aLook/blog/python-comparison/ibench-ouput/all-intel.out")$runs
time <- c()
for (test in json_data) {
  time <- c(time,test$stats$median)
}
df$intel <- time


df %>% melt() %>% ggplot(aes(x=test_name, y=value)) +
  geom_bar(aes(fill=variable), stat="identity", position = 'dodge')+
  theme_minimal() + 
  coord_flip()+ 
  scale_fill_brewer(palette='Paired')+
  ylab('Time (in seconds)') +
  xlab('Intel benchmarks') + ggtitle('Intel benchmarks')

ggsave("Documents/aLook/blog/python-comparison/pics/intel-benchmarks.jpg")
