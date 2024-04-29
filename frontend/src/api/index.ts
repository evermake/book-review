/**
 * Generated by orval v6.28.2 🍺
 * Do not edit manually.
 * Book Review Platform
 * OpenAPI spec version: 0.1.0
 */
import {
  useMutation,
  useQuery
} from '@tanstack/vue-query'
import type {
  MutationFunction,
  QueryFunction,
  QueryKey,
  UseMutationOptions,
  UseMutationReturnType,
  UseQueryOptions,
  UseQueryReturnType
} from '@tanstack/vue-query'
import * as axios from 'axios';
import type {
  AxiosError,
  AxiosRequestConfig,
  AxiosResponse
} from 'axios'
import {
  computed,
  unref
} from 'vue'
import type {
  MaybeRef
} from 'vue'
export type GetSingleUserUsersSingleGetParams = {
id?: number | null;
login?: string | null;
};

export type GetUsersUsersGetParams = {
login?: string | null;
};

export type CreateUserUsersPostParams = {
login: string;
password: string;
};

export type FindReviewsReviewsGetParams = {
book_id?: string | null;
user_id?: number | null;
};

export type DeleteReviewReviewsDeleteParams = {
book_id: string;
};

export type GetCoverCoversIdGetParams = {
size?: CoverSize;
};

export type SearchBooksBooksGetParams = {
query: string;
};

export type ValidationErrorLocItem = string | number;

export interface ValidationError {
  loc: ValidationErrorLocItem[];
  msg: string;
  type: string;
}

export interface User {
  created_at: string;
  id: number;
  login: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export type ReviewRequestCommentary = string | null;

export interface ReviewRequest {
  book_id: string;
  commentary: ReviewRequestCommentary;
  rating: number;
}

export type ReviewUpdatedAt = string | null;

export type ReviewCommentary = string | null;

export interface Review {
  book_id: string;
  commentary: ReviewCommentary;
  created_at: string;
  rating: number;
  updated_at: ReviewUpdatedAt;
  user_id: number;
}

export interface HTTPValidationError {
  detail?: ValidationError[];
}

export type CoverSize = typeof CoverSize[keyof typeof CoverSize];


// eslint-disable-next-line @typescript-eslint/no-redeclare
export const CoverSize = {
  S: 'S',
  M: 'M',
  L: 'L',
} as const;

export type BookPreviewFirstPublishmentDate = string | null;

export interface BookPreview {
  authors?: AuthorPreview[];
  first_publishment_date?: BookPreviewFirstPublishmentDate;
  id: string;
  languages?: string[];
  subjects?: string[];
  title: string;
}

export type BookDescription = string | null;

export type BookAuthorId = string | null;

export interface Book {
  author_id?: BookAuthorId;
  covers?: number[];
  description?: BookDescription;
  id: string;
  subjects?: string[];
  title: string;
}

export type BodyTokenTokenPostGrantType = string | null;

export type BodyTokenTokenPostClientSecret = string | null;

export type BodyTokenTokenPostClientId = string | null;

export interface BodyTokenTokenPost {
  client_id?: BodyTokenTokenPostClientId;
  client_secret?: BodyTokenTokenPostClientSecret;
  grant_type?: BodyTokenTokenPostGrantType;
  password: string;
  scope?: string;
  username: string;
}

export interface AuthorPreview {
  id: string;
  name: string;
}

export type AuthorWikipedia = string | null;

export type AuthorBio = string | null;

export interface Author {
  bio?: AuthorBio;
  key: string;
  name: string;
  wikipedia?: AuthorWikipedia;
}



type AwaitedInput<T> = PromiseLike<T> | T;

      type Awaited<O> = O extends AwaitedInput<infer T> ? T : never;



/**
 * @summary Health
 */
export const healthHealthGet = (
     options?: AxiosRequestConfig
 ): Promise<AxiosResponse<string>> => {
    
    return axios.default.get(
      `/health`,options
    );
  }


export const getHealthHealthGetQueryKey = () => {
    return ['health'] as const;
    }

    
export const getHealthHealthGetQueryOptions = <TData = Awaited<ReturnType<typeof healthHealthGet>>, TError = AxiosError<unknown>>( options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof healthHealthGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getHealthHealthGetQueryKey();

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof healthHealthGet>>> = ({ signal }) => healthHealthGet({ signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof healthHealthGet>>, TError, TData> 
}

export type HealthHealthGetQueryResult = NonNullable<Awaited<ReturnType<typeof healthHealthGet>>>
export type HealthHealthGetQueryError = AxiosError<unknown>

/**
 * @summary Health
 */
export const useHealthHealthGet = <TData = Awaited<ReturnType<typeof healthHealthGet>>, TError = AxiosError<unknown>>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof healthHealthGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getHealthHealthGetQueryOptions(options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Token
 */
export const tokenTokenPost = (
    bodyTokenTokenPost: MaybeRef<BodyTokenTokenPost>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<Token>> => {const formUrlEncoded = new URLSearchParams();
if(bodyTokenTokenPost.grant_type !== undefined) {
 formUrlEncoded.append('grant_type', bodyTokenTokenPost.grant_type)
 }
formUrlEncoded.append('username', bodyTokenTokenPost.username)
formUrlEncoded.append('password', bodyTokenTokenPost.password)
if(bodyTokenTokenPost.scope !== undefined) {
 formUrlEncoded.append('scope', bodyTokenTokenPost.scope)
 }
if(bodyTokenTokenPost.client_id !== undefined) {
 formUrlEncoded.append('client_id', bodyTokenTokenPost.client_id)
 }
if(bodyTokenTokenPost.client_secret !== undefined) {
 formUrlEncoded.append('client_secret', bodyTokenTokenPost.client_secret)
 }

    bodyTokenTokenPost = unref(bodyTokenTokenPost);
    return axios.default.post(
      `/token`,
      formUrlEncoded,options
    );
  }



export const getTokenTokenPostMutationOptions = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof tokenTokenPost>>, TError,{data: BodyTokenTokenPost}, TContext>, axios?: AxiosRequestConfig}
): UseMutationOptions<Awaited<ReturnType<typeof tokenTokenPost>>, TError,{data: BodyTokenTokenPost}, TContext> => {
const {mutation: mutationOptions, axios: axiosOptions} = options ?? {};

      


      const mutationFn: MutationFunction<Awaited<ReturnType<typeof tokenTokenPost>>, {data: BodyTokenTokenPost}> = (props) => {
          const {data} = props ?? {};

          return  tokenTokenPost(data,axiosOptions)
        }

        


  return  { mutationFn, ...mutationOptions }}

    export type TokenTokenPostMutationResult = NonNullable<Awaited<ReturnType<typeof tokenTokenPost>>>
    export type TokenTokenPostMutationBody = BodyTokenTokenPost
    export type TokenTokenPostMutationError = AxiosError<HTTPValidationError>

    /**
 * @summary Token
 */
export const useTokenTokenPost = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof tokenTokenPost>>, TError,{data: BodyTokenTokenPost}, TContext>, axios?: AxiosRequestConfig}
): UseMutationReturnType<
        Awaited<ReturnType<typeof tokenTokenPost>>,
        TError,
        {data: BodyTokenTokenPost},
        TContext
      > => {

      const mutationOptions = getTokenTokenPostMutationOptions(options);

      return useMutation(mutationOptions);
    }
    
/**
 * @summary Search Books
 */
export const searchBooksBooksGet = (
    params: MaybeRef<SearchBooksBooksGetParams>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<BookPreview[]>> => {
    params = unref(params);
    return axios.default.get(
      `/books`,{
    ...options,
        params: {...unref(params), ...options?.params},}
    );
  }


export const getSearchBooksBooksGetQueryKey = (params: MaybeRef<SearchBooksBooksGetParams>,) => {
    return ['books', ...(params ? [params]: [])] as const;
    }

    
export const getSearchBooksBooksGetQueryOptions = <TData = Awaited<ReturnType<typeof searchBooksBooksGet>>, TError = AxiosError<HTTPValidationError>>(params: MaybeRef<SearchBooksBooksGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof searchBooksBooksGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getSearchBooksBooksGetQueryKey(params);

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof searchBooksBooksGet>>> = ({ signal }) => searchBooksBooksGet(params, { signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof searchBooksBooksGet>>, TError, TData> 
}

export type SearchBooksBooksGetQueryResult = NonNullable<Awaited<ReturnType<typeof searchBooksBooksGet>>>
export type SearchBooksBooksGetQueryError = AxiosError<HTTPValidationError>

/**
 * @summary Search Books
 */
export const useSearchBooksBooksGet = <TData = Awaited<ReturnType<typeof searchBooksBooksGet>>, TError = AxiosError<HTTPValidationError>>(
 params: MaybeRef<SearchBooksBooksGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof searchBooksBooksGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getSearchBooksBooksGetQueryOptions(params,options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Get Book
 */
export const getBookBooksIdGet = (
    id: MaybeRef<string>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<Book>> => {
    id = unref(id);
    return axios.default.get(
      `/books/${id}`,options
    );
  }


export const getGetBookBooksIdGetQueryKey = (id: MaybeRef<string>,) => {
    return ['books',id] as const;
    }

    
export const getGetBookBooksIdGetQueryOptions = <TData = Awaited<ReturnType<typeof getBookBooksIdGet>>, TError = AxiosError<HTTPValidationError>>(id: MaybeRef<string>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getBookBooksIdGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getGetBookBooksIdGetQueryKey(id);

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof getBookBooksIdGet>>> = ({ signal }) => getBookBooksIdGet(id, { signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, enabled: computed(() => !!(unref(id))), ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof getBookBooksIdGet>>, TError, TData> 
}

export type GetBookBooksIdGetQueryResult = NonNullable<Awaited<ReturnType<typeof getBookBooksIdGet>>>
export type GetBookBooksIdGetQueryError = AxiosError<HTTPValidationError>

/**
 * @summary Get Book
 */
export const useGetBookBooksIdGet = <TData = Awaited<ReturnType<typeof getBookBooksIdGet>>, TError = AxiosError<HTTPValidationError>>(
 id: MaybeRef<string>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getBookBooksIdGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getGetBookBooksIdGetQueryOptions(id,options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Get Author
 */
export const getAuthorAuthorsIdGet = (
    id: MaybeRef<string>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<Author>> => {
    id = unref(id);
    return axios.default.get(
      `/authors/${id}`,options
    );
  }


export const getGetAuthorAuthorsIdGetQueryKey = (id: MaybeRef<string>,) => {
    return ['authors',id] as const;
    }

    
export const getGetAuthorAuthorsIdGetQueryOptions = <TData = Awaited<ReturnType<typeof getAuthorAuthorsIdGet>>, TError = AxiosError<HTTPValidationError>>(id: MaybeRef<string>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getAuthorAuthorsIdGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getGetAuthorAuthorsIdGetQueryKey(id);

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof getAuthorAuthorsIdGet>>> = ({ signal }) => getAuthorAuthorsIdGet(id, { signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, enabled: computed(() => !!(unref(id))), ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof getAuthorAuthorsIdGet>>, TError, TData> 
}

export type GetAuthorAuthorsIdGetQueryResult = NonNullable<Awaited<ReturnType<typeof getAuthorAuthorsIdGet>>>
export type GetAuthorAuthorsIdGetQueryError = AxiosError<HTTPValidationError>

/**
 * @summary Get Author
 */
export const useGetAuthorAuthorsIdGet = <TData = Awaited<ReturnType<typeof getAuthorAuthorsIdGet>>, TError = AxiosError<HTTPValidationError>>(
 id: MaybeRef<string>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getAuthorAuthorsIdGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getGetAuthorAuthorsIdGetQueryOptions(id,options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Get Cover
 */
export const getCoverCoversIdGet = (
    id: MaybeRef<number>,
    params?: MaybeRef<GetCoverCoversIdGetParams>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<unknown>> => {
    id = unref(id);
params = unref(params);
    return axios.default.get(
      `/covers/${id}`,{
    ...options,
        params: {...unref(params), ...options?.params},}
    );
  }


export const getGetCoverCoversIdGetQueryKey = (id: MaybeRef<number>,
    params?: MaybeRef<GetCoverCoversIdGetParams>,) => {
    return ['covers',id, ...(params ? [params]: [])] as const;
    }

    
export const getGetCoverCoversIdGetQueryOptions = <TData = Awaited<ReturnType<typeof getCoverCoversIdGet>>, TError = AxiosError<HTTPValidationError>>(id: MaybeRef<number>,
    params?: MaybeRef<GetCoverCoversIdGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getCoverCoversIdGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getGetCoverCoversIdGetQueryKey(id,params);

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof getCoverCoversIdGet>>> = ({ signal }) => getCoverCoversIdGet(id,params, { signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, enabled: computed(() => !!(unref(id))), ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof getCoverCoversIdGet>>, TError, TData> 
}

export type GetCoverCoversIdGetQueryResult = NonNullable<Awaited<ReturnType<typeof getCoverCoversIdGet>>>
export type GetCoverCoversIdGetQueryError = AxiosError<HTTPValidationError>

/**
 * @summary Get Cover
 */
export const useGetCoverCoversIdGet = <TData = Awaited<ReturnType<typeof getCoverCoversIdGet>>, TError = AxiosError<HTTPValidationError>>(
 id: MaybeRef<number>,
    params?: MaybeRef<GetCoverCoversIdGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getCoverCoversIdGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getGetCoverCoversIdGetQueryOptions(id,params,options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Create Or Update Review
 */
export const createOrUpdateReviewReviewsPost = (
    reviewRequest: MaybeRef<ReviewRequest>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<unknown>> => {
    reviewRequest = unref(reviewRequest);
    return axios.default.post(
      `/reviews`,
      reviewRequest,options
    );
  }



export const getCreateOrUpdateReviewReviewsPostMutationOptions = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof createOrUpdateReviewReviewsPost>>, TError,{data: ReviewRequest}, TContext>, axios?: AxiosRequestConfig}
): UseMutationOptions<Awaited<ReturnType<typeof createOrUpdateReviewReviewsPost>>, TError,{data: ReviewRequest}, TContext> => {
const {mutation: mutationOptions, axios: axiosOptions} = options ?? {};

      


      const mutationFn: MutationFunction<Awaited<ReturnType<typeof createOrUpdateReviewReviewsPost>>, {data: ReviewRequest}> = (props) => {
          const {data} = props ?? {};

          return  createOrUpdateReviewReviewsPost(data,axiosOptions)
        }

        


  return  { mutationFn, ...mutationOptions }}

    export type CreateOrUpdateReviewReviewsPostMutationResult = NonNullable<Awaited<ReturnType<typeof createOrUpdateReviewReviewsPost>>>
    export type CreateOrUpdateReviewReviewsPostMutationBody = ReviewRequest
    export type CreateOrUpdateReviewReviewsPostMutationError = AxiosError<HTTPValidationError>

    /**
 * @summary Create Or Update Review
 */
export const useCreateOrUpdateReviewReviewsPost = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof createOrUpdateReviewReviewsPost>>, TError,{data: ReviewRequest}, TContext>, axios?: AxiosRequestConfig}
): UseMutationReturnType<
        Awaited<ReturnType<typeof createOrUpdateReviewReviewsPost>>,
        TError,
        {data: ReviewRequest},
        TContext
      > => {

      const mutationOptions = getCreateOrUpdateReviewReviewsPostMutationOptions(options);

      return useMutation(mutationOptions);
    }
    
/**
 * @summary Delete Review
 */
export const deleteReviewReviewsDelete = (
    params: MaybeRef<DeleteReviewReviewsDeleteParams>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<unknown>> => {
    params = unref(params);
    return axios.default.delete(
      `/reviews`,{
    ...options,
        params: {...unref(params), ...options?.params},}
    );
  }



export const getDeleteReviewReviewsDeleteMutationOptions = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof deleteReviewReviewsDelete>>, TError,{params: DeleteReviewReviewsDeleteParams}, TContext>, axios?: AxiosRequestConfig}
): UseMutationOptions<Awaited<ReturnType<typeof deleteReviewReviewsDelete>>, TError,{params: DeleteReviewReviewsDeleteParams}, TContext> => {
const {mutation: mutationOptions, axios: axiosOptions} = options ?? {};

      


      const mutationFn: MutationFunction<Awaited<ReturnType<typeof deleteReviewReviewsDelete>>, {params: DeleteReviewReviewsDeleteParams}> = (props) => {
          const {params} = props ?? {};

          return  deleteReviewReviewsDelete(params,axiosOptions)
        }

        


  return  { mutationFn, ...mutationOptions }}

    export type DeleteReviewReviewsDeleteMutationResult = NonNullable<Awaited<ReturnType<typeof deleteReviewReviewsDelete>>>
    
    export type DeleteReviewReviewsDeleteMutationError = AxiosError<HTTPValidationError>

    /**
 * @summary Delete Review
 */
export const useDeleteReviewReviewsDelete = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof deleteReviewReviewsDelete>>, TError,{params: DeleteReviewReviewsDeleteParams}, TContext>, axios?: AxiosRequestConfig}
): UseMutationReturnType<
        Awaited<ReturnType<typeof deleteReviewReviewsDelete>>,
        TError,
        {params: DeleteReviewReviewsDeleteParams},
        TContext
      > => {

      const mutationOptions = getDeleteReviewReviewsDeleteMutationOptions(options);

      return useMutation(mutationOptions);
    }
    
/**
 * @summary Find Reviews
 */
export const findReviewsReviewsGet = (
    params?: MaybeRef<FindReviewsReviewsGetParams>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<Review[]>> => {
    params = unref(params);
    return axios.default.get(
      `/reviews`,{
    ...options,
        params: {...unref(params), ...options?.params},}
    );
  }


export const getFindReviewsReviewsGetQueryKey = (params?: MaybeRef<FindReviewsReviewsGetParams>,) => {
    return ['reviews', ...(params ? [params]: [])] as const;
    }

    
export const getFindReviewsReviewsGetQueryOptions = <TData = Awaited<ReturnType<typeof findReviewsReviewsGet>>, TError = AxiosError<HTTPValidationError>>(params?: MaybeRef<FindReviewsReviewsGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof findReviewsReviewsGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getFindReviewsReviewsGetQueryKey(params);

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof findReviewsReviewsGet>>> = ({ signal }) => findReviewsReviewsGet(params, { signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof findReviewsReviewsGet>>, TError, TData> 
}

export type FindReviewsReviewsGetQueryResult = NonNullable<Awaited<ReturnType<typeof findReviewsReviewsGet>>>
export type FindReviewsReviewsGetQueryError = AxiosError<HTTPValidationError>

/**
 * @summary Find Reviews
 */
export const useFindReviewsReviewsGet = <TData = Awaited<ReturnType<typeof findReviewsReviewsGet>>, TError = AxiosError<HTTPValidationError>>(
 params?: MaybeRef<FindReviewsReviewsGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof findReviewsReviewsGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getFindReviewsReviewsGetQueryOptions(params,options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Create User
 */
export const createUserUsersPost = (
    params: MaybeRef<CreateUserUsersPostParams>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<User>> => {
    params = unref(params);
    return axios.default.post(
      `/users`,undefined,{
    ...options,
        params: {...unref(params), ...options?.params},}
    );
  }



export const getCreateUserUsersPostMutationOptions = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof createUserUsersPost>>, TError,{params: CreateUserUsersPostParams}, TContext>, axios?: AxiosRequestConfig}
): UseMutationOptions<Awaited<ReturnType<typeof createUserUsersPost>>, TError,{params: CreateUserUsersPostParams}, TContext> => {
const {mutation: mutationOptions, axios: axiosOptions} = options ?? {};

      


      const mutationFn: MutationFunction<Awaited<ReturnType<typeof createUserUsersPost>>, {params: CreateUserUsersPostParams}> = (props) => {
          const {params} = props ?? {};

          return  createUserUsersPost(params,axiosOptions)
        }

        


  return  { mutationFn, ...mutationOptions }}

    export type CreateUserUsersPostMutationResult = NonNullable<Awaited<ReturnType<typeof createUserUsersPost>>>
    
    export type CreateUserUsersPostMutationError = AxiosError<HTTPValidationError>

    /**
 * @summary Create User
 */
export const useCreateUserUsersPost = <TError = AxiosError<HTTPValidationError>,
    TContext = unknown>(options?: { mutation?:UseMutationOptions<Awaited<ReturnType<typeof createUserUsersPost>>, TError,{params: CreateUserUsersPostParams}, TContext>, axios?: AxiosRequestConfig}
): UseMutationReturnType<
        Awaited<ReturnType<typeof createUserUsersPost>>,
        TError,
        {params: CreateUserUsersPostParams},
        TContext
      > => {

      const mutationOptions = getCreateUserUsersPostMutationOptions(options);

      return useMutation(mutationOptions);
    }
    
/**
 * @summary Get Users
 */
export const getUsersUsersGet = (
    params?: MaybeRef<GetUsersUsersGetParams>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<User[]>> => {
    params = unref(params);
    return axios.default.get(
      `/users`,{
    ...options,
        params: {...unref(params), ...options?.params},}
    );
  }


export const getGetUsersUsersGetQueryKey = (params?: MaybeRef<GetUsersUsersGetParams>,) => {
    return ['users', ...(params ? [params]: [])] as const;
    }

    
export const getGetUsersUsersGetQueryOptions = <TData = Awaited<ReturnType<typeof getUsersUsersGet>>, TError = AxiosError<HTTPValidationError>>(params?: MaybeRef<GetUsersUsersGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getUsersUsersGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getGetUsersUsersGetQueryKey(params);

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof getUsersUsersGet>>> = ({ signal }) => getUsersUsersGet(params, { signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof getUsersUsersGet>>, TError, TData> 
}

export type GetUsersUsersGetQueryResult = NonNullable<Awaited<ReturnType<typeof getUsersUsersGet>>>
export type GetUsersUsersGetQueryError = AxiosError<HTTPValidationError>

/**
 * @summary Get Users
 */
export const useGetUsersUsersGet = <TData = Awaited<ReturnType<typeof getUsersUsersGet>>, TError = AxiosError<HTTPValidationError>>(
 params?: MaybeRef<GetUsersUsersGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getUsersUsersGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getGetUsersUsersGetQueryOptions(params,options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Get Single User
 */
export const getSingleUserUsersSingleGet = (
    params?: MaybeRef<GetSingleUserUsersSingleGetParams>, options?: AxiosRequestConfig
 ): Promise<AxiosResponse<User>> => {
    params = unref(params);
    return axios.default.get(
      `/users/single`,{
    ...options,
        params: {...unref(params), ...options?.params},}
    );
  }


export const getGetSingleUserUsersSingleGetQueryKey = (params?: MaybeRef<GetSingleUserUsersSingleGetParams>,) => {
    return ['users','single', ...(params ? [params]: [])] as const;
    }

    
export const getGetSingleUserUsersSingleGetQueryOptions = <TData = Awaited<ReturnType<typeof getSingleUserUsersSingleGet>>, TError = AxiosError<HTTPValidationError>>(params?: MaybeRef<GetSingleUserUsersSingleGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getSingleUserUsersSingleGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getGetSingleUserUsersSingleGetQueryKey(params);

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof getSingleUserUsersSingleGet>>> = ({ signal }) => getSingleUserUsersSingleGet(params, { signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof getSingleUserUsersSingleGet>>, TError, TData> 
}

export type GetSingleUserUsersSingleGetQueryResult = NonNullable<Awaited<ReturnType<typeof getSingleUserUsersSingleGet>>>
export type GetSingleUserUsersSingleGetQueryError = AxiosError<HTTPValidationError>

/**
 * @summary Get Single User
 */
export const useGetSingleUserUsersSingleGet = <TData = Awaited<ReturnType<typeof getSingleUserUsersSingleGet>>, TError = AxiosError<HTTPValidationError>>(
 params?: MaybeRef<GetSingleUserUsersSingleGetParams>, options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getSingleUserUsersSingleGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getGetSingleUserUsersSingleGetQueryOptions(params,options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Get Current User
 */
export const getCurrentUserUsersMeGet = (
     options?: AxiosRequestConfig
 ): Promise<AxiosResponse<User>> => {
    
    return axios.default.get(
      `/users/me`,options
    );
  }


export const getGetCurrentUserUsersMeGetQueryKey = () => {
    return ['users','me'] as const;
    }

    
export const getGetCurrentUserUsersMeGetQueryOptions = <TData = Awaited<ReturnType<typeof getCurrentUserUsersMeGet>>, TError = AxiosError<unknown>>( options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getCurrentUserUsersMeGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getGetCurrentUserUsersMeGetQueryKey();

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof getCurrentUserUsersMeGet>>> = ({ signal }) => getCurrentUserUsersMeGet({ signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof getCurrentUserUsersMeGet>>, TError, TData> 
}

export type GetCurrentUserUsersMeGetQueryResult = NonNullable<Awaited<ReturnType<typeof getCurrentUserUsersMeGet>>>
export type GetCurrentUserUsersMeGetQueryError = AxiosError<unknown>

/**
 * @summary Get Current User
 */
export const useGetCurrentUserUsersMeGet = <TData = Awaited<ReturnType<typeof getCurrentUserUsersMeGet>>, TError = AxiosError<unknown>>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getCurrentUserUsersMeGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getGetCurrentUserUsersMeGetQueryOptions(options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




/**
 * @summary Get Current User Reviews
 */
export const getCurrentUserReviewsUsersMeReviewsGet = (
     options?: AxiosRequestConfig
 ): Promise<AxiosResponse<Review[]>> => {
    
    return axios.default.get(
      `/users/me/reviews`,options
    );
  }


export const getGetCurrentUserReviewsUsersMeReviewsGetQueryKey = () => {
    return ['users','me','reviews'] as const;
    }

    
export const getGetCurrentUserReviewsUsersMeReviewsGetQueryOptions = <TData = Awaited<ReturnType<typeof getCurrentUserReviewsUsersMeReviewsGet>>, TError = AxiosError<unknown>>( options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getCurrentUserReviewsUsersMeReviewsGet>>, TError, TData>>, axios?: AxiosRequestConfig}
) => {

const {query: queryOptions, axios: axiosOptions} = options ?? {};

  const queryKey =  getGetCurrentUserReviewsUsersMeReviewsGetQueryKey();

  

    const queryFn: QueryFunction<Awaited<ReturnType<typeof getCurrentUserReviewsUsersMeReviewsGet>>> = ({ signal }) => getCurrentUserReviewsUsersMeReviewsGet({ signal, ...axiosOptions });

      

      

   return  { queryKey, queryFn, ...queryOptions} as UseQueryOptions<Awaited<ReturnType<typeof getCurrentUserReviewsUsersMeReviewsGet>>, TError, TData> 
}

export type GetCurrentUserReviewsUsersMeReviewsGetQueryResult = NonNullable<Awaited<ReturnType<typeof getCurrentUserReviewsUsersMeReviewsGet>>>
export type GetCurrentUserReviewsUsersMeReviewsGetQueryError = AxiosError<unknown>

/**
 * @summary Get Current User Reviews
 */
export const useGetCurrentUserReviewsUsersMeReviewsGet = <TData = Awaited<ReturnType<typeof getCurrentUserReviewsUsersMeReviewsGet>>, TError = AxiosError<unknown>>(
  options?: { query?:Partial<UseQueryOptions<Awaited<ReturnType<typeof getCurrentUserReviewsUsersMeReviewsGet>>, TError, TData>>, axios?: AxiosRequestConfig}

  ): UseQueryReturnType<TData, TError> & { queryKey: QueryKey } => {

  const queryOptions = getGetCurrentUserReviewsUsersMeReviewsGetQueryOptions(options)

  const query = useQuery(queryOptions) as UseQueryReturnType<TData, TError> & { queryKey: QueryKey };

  query.queryKey = unref(queryOptions).queryKey as QueryKey;

  return query;
}




