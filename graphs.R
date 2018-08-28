library(readr)
conda <- as.data.frame(t(read_csv("Documents/aLook/blog/python-comparison/timetest-output/conda.csv", 
                  col_names = FALSE, col_types = cols(X1 = col_skip()))), stringsAsFactors = FALSE)

clean <- as.data.frame(t(read_csv("Documents/aLook/blog/python-comparison/timetest-output/clean.csv", 
                  col_names = FALSE, col_types = cols(X1 = col_skip()))), stringsAsFactors = FALSE)


intel <- as.data.frame(t(read_csv("Documents/aLook/blog/python-comparison/timetest-output/intel.csv", 
                  col_names = FALSE, col_types = cols(X1 = col_skip()))), stringsAsFactors = FALSE)

library(reshape2)
library(tidyverse)


columns <- c('test', 'setup', 'nrows', 'ntests', 'runlength_mean', 'runlength_best', 'run_usec_mean',  'run_usec_min')
colnames(conda) <- columns
colnames(clean) <- columns
colnames(intel) <- columns

create_graph_data<-function(setup_name, nrows_len){
  if (setup_name=='intel'){
    df1 <- clean %>% filter(setup==setup_name) %>% 
      filter(str_detect(test, 'array')) %>%
      select('test', 'nrows', 'run_usec_min')
  } else{
    df1 <- clean %>% filter(setup==setup_name) %>%
      select('test', 'nrows', 'run_usec_min')
  }
  
  df2 <- conda %>% filter(setup==setup_name) %>% select('test', 'nrows', 'run_usec_min')
  df3 <- intel %>% filter(setup==setup_name) %>% select('test', 'nrows', 'run_usec_min')
  
  a <- df1 %>% 
    left_join(df2, by=c('test', 'nrows'), suffix=c('_clean', '_conda')) %>% 
    left_join(df3, by=c('test', 'nrows'), suffix=c('', '_intel')) 
  
  colnames(a) <- c('test', 'nrows', 'clean_ubuntu', 'conda_dist', 'intel_dist')
  a <- a %>% melt(id=c('test', 'nrows')) %>% filter(nrows==nrows_len)
  return(a)
}

p <- ggplot(create_graph_data('intel', '1000000'), aes(x=test, y=as.numeric(value))) +
  geom_bar(aes(fill=variable), stat="identity", position = 'dodge') +
  ylab('Best time (μsec)') + xlab('Speed test with array length of 1 000 000') +
  theme_minimal() + 
  scale_fill_brewer(palette='Paired') + ggtitle('Tests on numpy arrays')
ggsave("Documents/aLook/blog/python-comparison/pics/numpy.jpg", p)

data_graph <- create_graph_data('pandas', '1000000') %>% 
  filter(test %in% c('array apply', 'array or array', 'array and array', 'array+array','array-array','subseries+subseries'))
p <- ggplot(data_graph, aes(x=test, y=as.numeric(value))) +
  geom_bar(aes(fill=variable), stat="identity", position = 'dodge')+ 
  ylab('Best time (μsec)') + xlab('Speed test with array length of 1 000 000') +
  theme_minimal() + scale_fill_brewer(palette='Paired') + ggtitle('Tests on pandas DataFrames')
ggsave("Documents/aLook/blog/python-comparison/pics/pandas.jpg", p)

data_graph <- create_graph_data('sklearn', '100000') 
p <- ggplot(data_graph, aes(x=test, y=as.numeric(value))) +
  geom_bar(aes(fill=variable), stat="identity", position = 'dodge')+ 
  ylab('Best time (μsec)') + xlab('Speed test with array length of 100 000') +
  theme_minimal() + scale_fill_brewer(palette='Paired') + ggtitle('Tests with sklearn')

ggsave("Documents/aLook/blog/python-comparison/pics/sklearn.jpg", p)